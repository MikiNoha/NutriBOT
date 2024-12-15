
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
# test = os.getenv('OPENAI_API_KEY')
# print(test)

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# print(client)

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Replace with your desired model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact about Python programming."}
    ]
)

# Print the assistant's reply
print(response.choices[0].message.content)



