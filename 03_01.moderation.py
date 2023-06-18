import os
import openai
import requests
import json
from hello_api import check_response_code, get_token, get_task, send_answer
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORGANIZATION_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
apikey = os.getenv("API_KEY")
url = "https://zadania.aidevs.pl"
endpoint = "/token/moderation"


def check_moderation_status(data):
  flagged_results = []
  data = data['input']

  for item in data:
    response = openai.Moderation.create(
      input=item,
    )
    flagged = response['results'][0]['flagged']
    flagged_results.append(1 if flagged else 0)

  print(flagged_results)
  return flagged_results


token = get_token(url, apikey, endpoint)

task = get_task(token)

result = check_moderation_status(task)

send_answers(result)