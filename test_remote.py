import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("REMOTE_API_KEY"),
    base_url=os.environ.get("REMOTE_BASE_URL"),
)
try:
    r = client.chat.completions.create(
        model="accounts/fireworks/models/deepseek-v4-pro",
        messages=[{"role": "user", "content": "hello"}],
        max_tokens=10
    )
    print("SUCCESS!", r.choices[0].message.content)
except Exception as e:
    print("FAILED!", e)
