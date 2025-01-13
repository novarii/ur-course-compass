import openai
from openai_client import OpenAIClient
from ai.course_data import course_data


# Initialize and use the client
client = OpenAIClient("OWNKEYHERE")
formatted_schedule = client.get_formatted_schedule(course_data)
print(formatted_schedule)
