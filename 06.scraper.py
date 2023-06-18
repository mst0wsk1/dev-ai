import os
import openai
import requests
import json
from hello_api import check_response_code, get_token, get_task, send_answer, create_completion
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORGANIZATION_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
apikey = os.getenv("API_KEY")
url = os.getenv("URL")
endpoint = "/token/scraper"

try:
  token = get_token(url, apikey, endpoint)
  data = get_task(token)

  question = data["question"]
  prompt = f"""
  Odpowiedz w języku polskim na poniższe pytanie.

  ### pytanie
  {question}
  """

  answer = create_completion(prompt)

  send_answer(answer, token)
except Exception as e:
  print(f"Wystąpił nieoczekiwany błąd: {e}")