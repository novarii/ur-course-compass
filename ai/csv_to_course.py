import csv
from datetime import datetime
from pprint import pformat


def transform_csv_to_course_data(csv_file: str) -> str:
    """
    Transform CSV course data into Python code format.
    """
    required_courses = {
        "CSC 171", "CSC 172", "CSC 173",
        "CSC 242", "CSC 252", "CSC 254",
        "CSC 280", "CSC 282"
    }

    course_data = {
        "custom_courses": {
            "fall": [],
            "spring": []
        },
        "required_courses": {
            "fall": [],
            "spring": []
        },
        "Goals": "I want to learn ML and datastructures",
        "ClassesLeft": 6,
        "NextSem": 4
    }

    def parse_time(time_str: str) -> str:
        try:
            time_obj = datetime.strptime(time_str, '%I%M %p')
            return time_obj.strftime('%I:%M %p').lstrip('0')
        except:
            return time_str

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row['Code'].startswith('CSC'):
                    continue

                base_code = row['Code'].split('-')[0].strip()

                course = {
                    "dep": "CSC",
                    "num": base_code.split()[1],
                    "title": row['Title'],
                    "prereq": row['Prereqs'] if row['Prereqs'] else "N/A",
                    "credit": row['Credits'],
                    "start": parse_time(row['Begin']),
                    "end": parse_time(row['End']),
                    "term": row['Term']
                }

                is_required = base_code in required_courses
                category = "required_courses" if is_required else "custom_courses"
                term = row['Term'].lower()

                existing_courses = [c['num'] for c in course_data[category][term]]
                if course['num'] not in existing_courses:
                    course_data[category][term].append(course)
    except UnicodeDecodeError:
        with open(csv_file, 'r', encoding='latin-1') as file:
            # ... same processing as above ...
            pass

    # Generate Python code
    python_code = f"""# course_data.py

course_data = {pformat(course_data, indent=4)}
"""

    return python_code


if __name__ == "__main__":
    # Transform the data
    python_code = transform_csv_to_course_data('courses.csv')

    # Save to Python file
    with open('course_data.py', 'w', encoding='utf-8') as f:
        f.write(python_code)