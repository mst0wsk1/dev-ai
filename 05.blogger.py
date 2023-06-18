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
endpoint = "/token/blogger"

token = get_token(url, apikey, endpoint)
data = get_task(token)
text = "\n".join(data['blog'])

prompt = f"""
Napisz 2-3 zdania dla każdego z czterech zagadnień wymienionych poniżej. Odpowiedź zwróć jako tablicę w formacie JSON z czteroma rzędami w formie stringów.

### zagadnienia
{text}
"""

answer = create_completion(text)
send_answer(answer, token)
