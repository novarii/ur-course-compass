from typing import Dict, List, Any, Set
from collections import defaultdict
import json
import math
import openai

from ai.prompts import PromptTemplates
from ai.schedule_formatter import ScheduleFormatter
from ai.sort_prereq import PrerequisiteGraph


class OpenAIClient:
    def __init__(self, api_key: str):
        """Initialize OpenAI client with API key."""
        openai.api_key = api_key
        self.completed_courses: Set[str] = set()  # Track completed courses

    def generate_schedule(self, course_data: Dict[str, Any]) -> Dict[int, List[str]]:
        """Generate course schedule with prerequisite checking."""
        try:
            complete_schedule = {}
            current_data = course_data.copy()

            # Initialize prerequisite graph
            prereq_graph = PrerequisiteGraph(course_data)
            prereq_graph.topological_sort()  # Ensure valid prerequisite order

            # Calculate scheduling parameters
            total_required = (len(current_data['required_courses']['fall']) +
                              len(current_data['required_courses']['spring']))
            total_custom = current_data['ClassesLeft']
            total_courses = total_required + total_custom

            remaining_terms = 9 - current_data['NextSem']
            target_per_term = math.ceil(total_courses / remaining_terms)

            current_data['TargetCoursesPerTerm'] = target_per_term
            current_data['RemainingCourses'] = total_courses

            # Add prerequisite information to the data
            current_data['available_courses'] = prereq_graph.get_available_courses(self.completed_courses)
            current_data['prerequisites_map'] = {
                course_id: prereq_graph.get_prerequisites(course_id)
                for course_id in prereq_graph.course_info.keys()
            }

            # Generate schedule term by term
            for term in range(current_data['NextSem'], 9):
                current_data['NextSem'] = term
                remaining_terms = 9 - term

                if remaining_terms > 0:
                    current_data['TargetCoursesPerTerm'] = math.ceil(
                        current_data['RemainingCourses'] / remaining_terms
                    )

                # Get the prompt for this term
                prompt = PromptTemplates.create_schedule_prompt(current_data)

                response = openai.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=1000,
                    response_format={"type": "json_object"}
                )

                # Parse and validate the schedule
                term_schedule = json.loads(response.choices[0].message.content)

                # Validate prerequisites for scheduled courses
                validated_schedule = self._validate_prerequisites(
                    term_schedule,
                    prereq_graph
                )

                # Update the complete schedule
                complete_schedule.update(validated_schedule)

                # Update completed courses and course lists
                self._update_course_lists(current_data, validated_schedule)
                self._update_completed_courses(validated_schedule)

                # Update available courses for next term
                current_data['available_courses'] = prereq_graph.get_available_courses(
                    self.completed_courses
                )

                # Update remaining courses count
                scheduled_this_term = sum(len(courses) for courses in validated_schedule.values())
                current_data['RemainingCourses'] -= scheduled_this_term

            return complete_schedule

        except Exception as e:
            print(f"Error generating schedule: {str(e)}")
            return {}

    def get_formatted_schedule(self, course_data: Dict[str, Any]) -> str:
        """Generate and format the schedule."""
        schedule = self.generate_schedule(course_data)
        return ScheduleFormatter.format_schedule(schedule)


    def _validate_prerequisites(
            self,
            term_schedule: Dict[str, List[str]],
            prereq_graph: PrerequisiteGraph
    ) -> Dict[str, List[str]]:
        """Validate and filter courses based on prerequisites."""
        validated_schedule = {}

        for term, courses in term_schedule.items():
            valid_courses = [
                course for course in courses
                if prereq_graph.can_take_course(course, self.completed_courses)
            ]
            if valid_courses:  # Only add term if it has valid courses
                validated_schedule[term] = valid_courses

        return validated_schedule

    def _update_completed_courses(self, term_schedule: Dict[str, List[str]]):
        """Update the set of completed courses."""
        for courses in term_schedule.values():
            self.completed_courses.update(courses)

    def _update_course_lists(self, data: Dict[str, Any], term_schedule: Dict[str, List[str]]):
        """Update available course lists after scheduling."""
        scheduled_courses = []
        for courses in term_schedule.values():
            scheduled_courses.extend(courses)

        def filter_courses(course_list):
            return [
                course for course in course_list
                if f"{course['dep']} {course['num']}" not in scheduled_courses
            ]

        # Update both required and custom course lists
        data['required_courses']['fall'] = filter_courses(data['required_courses']['fall'])
        data['required_courses']['spring'] = filter_courses(data['required_courses']['spring'])
        data['custom_courses']['fall'] = filter_courses(data['custom_courses']['fall'])
        data['custom_courses']['spring'] = filter_courses(data['custom_courses']['spring'])

        # Update ClassesLeft for custom courses
        scheduled_custom = sum(
            1 for course in scheduled_courses
            if any(
                f"{c['dep']} {c['num']}" == course
                for season_courses in data['custom_courses'].values()
                for c in season_courses
            )
        )
        data['ClassesLeft'] = max(0, data['ClassesLeft'] - scheduled_custom)