from collections import defaultdict
from typing import Dict, List, Set, Any


class PrerequisiteGraph:
    def __init__(self, course_data: Dict[str, Any]):
        self.graph = defaultdict(list)  # adjacency list
        self.in_degree = defaultdict(int)  # track incoming edges
        self.course_info = {}  # store full course info
        self.course_order = []  # topologically sorted order
        self.build_graph(course_data)

    def build_graph(self, course_data: Dict[str, Any]) -> None:
        """Build adjacency list from course data"""
        # First pass: collect all courses and their info
        for season in ['fall', 'spring']:
            for course_list in [course_data['required_courses'][season],
                                course_data['custom_courses'][season]]:
                for course in course_list:
                    course_id = f"{course['dep']} {course['num']}"
                    self.course_info[course_id] = course

                    # Initialize in_degree for all courses
                    if course_id not in self.in_degree:
                        self.in_degree[course_id] = 0

                    # Parse prerequisites
                    if course['prereq'] != 'N/A':
                        prereqs = [p.strip() for p in course['prereq'].split(',')]
                        for prereq in prereqs:
                            self.graph[prereq].append(course_id)
                            self.in_degree[course_id] += 1

    def topological_sort(self) -> List[str]:
        """Perform Kahn's algorithm for topological sorting"""
        result = []
        no_prereq = [
            course for course in self.course_info.keys()
            if self.in_degree[course] == 0
        ]

        while no_prereq:
            current = no_prereq.pop()
            result.append(current)

            # Reduce in_degree for all courses that depend on current
            for dependent in self.graph[current]:
                self.in_degree[dependent] -= 1
                if self.in_degree[dependent] == 0:
                    no_prereq.append(dependent)

        # Check if all courses were included (no cycles)
        if len(result) != len(self.course_info):
            raise ValueError("Prerequisite cycle detected")

        self.course_order = result
        return result

    def get_prerequisites(self, course_id: str) -> List[str]:
        """Get all prerequisites for a given course"""
        prereqs = set()

        def dfs(current: str) -> None:
            if current in self.course_info and 'prereq' in self.course_info[current]:
                course = self.course_info[current]
                if course['prereq'] != 'N/A':
                    for prereq in course['prereq'].split(','):
                        prereq = prereq.strip()
                        if prereq not in prereqs:
                            prereqs.add(prereq)
                            dfs(prereq)

        dfs(course_id)
        return list(prereqs)

    def can_take_course(self, course_id: str, completed_courses: Set[str]) -> bool:
        """Check if a course can be taken given completed courses"""
        if course_id not in self.course_info:
            return False

        prereqs = self.get_prerequisites(course_id)
        return all(prereq in completed_courses for prereq in prereqs)

    def get_available_courses(self, completed_courses: Set[str]) -> List[str]:
        """Get all courses that can be taken given completed courses"""
        available = []
        for course_id in self.course_info:
            if course_id not in completed_courses and self.can_take_course(course_id, completed_courses):
                available.append(course_id)
        return available