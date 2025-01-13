import json
from typing import Dict, Any


class PromptTemplates:
    @staticmethod
    def create_schedule_prompt(data: Dict[str, Any]) -> str:
        """Create a prompt for generating course schedule with prerequisites."""
        next_sem = data.get('NextSem', 7)
        classes_left = data.get('ClassesLeft', 0)
        goals = data.get('Goals', '')
        target_courses = data.get('TargetCoursesPerTerm', 4)
        remaining_courses = data.get('RemainingCourses', 0)
        available_courses = data.get('available_courses', [])
        prerequisites_map = data.get('prerequisites_map', {})

        is_fall_term = next_sem % 2 == 1
        season = "fall" if is_fall_term else "spring"

        required_courses = data['required_courses'][season]
        custom_courses = data['custom_courses'][season]

        # Format prerequisites for better readability
        prereq_info = json.dumps(prerequisites_map, indent=2)
        available_courses_str = json.dumps(available_courses, indent=2)

        prompt = f"""You are a course scheduling assistant. Create a course schedule for term {next_sem} ({season}) following these strict rules:

1. PREREQUISITES ARE CRITICAL:
   - You can ONLY schedule courses from this available courses list (these have their prerequisites met):
   {available_courses_str}

   - For reference, here are the prerequisites for all courses:
   {prereq_info}

2. CRITICAL BALANCE REQUIREMENT: 
   - You MUST schedule approximately {target_courses} courses this term
   - This ensures balanced distribution across remaining terms

3. Course Selection Rules:
   - Include required courses from the required_courses list first
   - Select up to {classes_left} courses from custom_courses that match goals: "{goals}"
   - Total courses scheduled should be close to {target_courses}

4. CRITICAL TIME CONFLICT RULE: 
   When adding any course, check for time conflicts. Two courses conflict if their time slots overlap.
   For example:
   - Course A: 9:00 AM - 10:15 AM conflicts with Course B: 9:30 AM - 10:45 AM
   - Course A: 2:00 PM - 3:15 PM conflicts with Course B: 3:00 PM - 4:15 PM

Scheduling Information:
- Total remaining courses to schedule: {remaining_courses}
- Target courses for this term: {target_courses}
- Available required courses for {season}: {len(required_courses)}
- Available custom courses for {season}: {len(custom_courses)}

Return the schedule in this exact JSON format:
{{
  "{next_sem}": ["DEP NUM", "DEP NUM", ...]
}}

Available Required Courses for {season}:
{json.dumps(required_courses, indent=2)}

Available Custom Courses for {season}:
{json.dumps(custom_courses, indent=2)}

Scheduling Process:
1. ONLY select courses from the available_courses list above
2. Aim to schedule {target_courses} courses this term
3. Start with required courses
4. Add custom courses that align with goals: "{goals}"
5. Check time conflicts before adding each course
6. Format course IDs as "DEP NUM" (e.g., "CSC 171")

Remember:
- You can ONLY schedule courses from the available_courses list
- Meeting the target number of courses ({target_courses}) is crucial
- Double-check time conflicts before adding ANY course
- Only output the JSON schedule for term {next_sem}
- Use correct format for course numbers (e.g., "CSC 171")
- Consider the student's goals when selecting custom courses"""

        return prompt