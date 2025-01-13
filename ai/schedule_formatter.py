class ScheduleFormatter:
    @staticmethod
    def format_schedule(schedule: dict) -> str:
        """Format the schedule in a simple, readable way."""
        terms = {
            4: "Fall Year 2",
            5: "Spring Year 2",
            6: "Fall Year 3",
            7: "Spring Year 3",
            8: "Fall Year 4",
            9: "Spring Year 4"
        }

        formatted_output = "Your Academic Schedule:\n" + "=" * 50 + "\n"

        for term_num in sorted(schedule.keys()):
            term_name = terms.get(int(term_num), f"Term {term_num}")
            formatted_output += f"\n{term_name}:\n" + "-" * 50 + "\n"

            if not schedule[term_num]:  # If term has no courses
                formatted_output += "No courses scheduled\n"
                continue

            for course_id in sorted(schedule[term_num]):
                formatted_output += f"{course_id}\n"

            formatted_output += "\n"

        return formatted_output


# Example usage:
schedule = {
    '4': ['CSC 171', 'CSC 391'],
    '5': ['CSC 172'],
    '6': ['CSC 242', 'CSC 280', 'CSC 282'],
    '7': ['CSC 173', 'CSC 174', 'CSC 220', 'CSC 299'],
    '8': ['CSC 286', 'CSC 320', 'CSC 344']
}

print(ScheduleFormatter.format_schedule(schedule))