import os
import openai
from hello_api import check_response_code, get_token, get_task, send_answer
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
apikey = os.getenv("API_KEY")
url = os.getenv("URL")
endpoint = "/token/inprompt"


def create_completion(prompt):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": prompt}
    ],
  )

  answer = response.choices[0].message.content

  return answer


def inprompt(name, data):
  found_element = None

  for element in data['input']:
      if element.startswith(name):
          found_element = element
          return found_element


token = get_token(url, apikey, endpoint)

data = get_task(token)

text = inprompt("Ernest", data)

answer = create_completion(text)

send_answer(answer, token)