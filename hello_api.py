import os
import openai
import requests
import json
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORGANIZATION_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
apikey = os.getenv("API_KEY")
url = os.getenv("URL")
endpoint = "/token/moderation"


def check_response_code(response_json):
  if response_json["code"] != 0:
    print("Błąd: kod odpowiedzi nie jest równy 0")
    exit()


def get_token(url, apikey, endpoint):
  try:
    response = requests.post(f"{url}{endpoint}", json={"apikey": apikey})
    response_json = response.json()
    check_response_code(response_json)
    token = response_json["token"]
    return token
  except requests.exceptions.RequestException as e:
    print(f"Błąd podczas wysyłania żądania: {e}")
    exit()


def get_task(token):
  try:
    response = requests.get(f"{url}/task/{token}")
    response_json = response.json()
    check_response_code(response_json)
    return response_json
  except requests.exceptions.RequestException as e:
    print(f"Błąd podczas pobierania zadania: {e}")
    exit()


def send_answer(data, token):
  try:
    response = requests.post(f"{url}/answer/{token}", json={"answer": data})
    print(response.text)
  except requests.exceptions.RequestException as e:
    print(f"Błąd podczas wysyłania odpowiedzi: {e}")


def create_completion(prompt):
  try:
      response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "user", "content": prompt}
          ],
      )
      answer = response.choices[0].message.content
      return answer

  except openai.error.APIError as e:
    # Handle API error here, e.g. retry or log
    print(f"OpenAI API returned an API Error: {e}")
    exit()
  except openai.error.APIConnectionError as e:
    # Handle connection error here
    print(f"Failed to connect to OpenAI API: {e}")
    exit()
  except openai.error.RateLimitError as e:
    # Handle rate limit error (we recommend using exponential backoff)
    print(f"OpenAI API request exceeded rate limit: {e}")
    exit()