import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

def generate_embedding(text: str):
    resp = client.embeddings.create(
        model=os.getenv("MODEL"),
        input=[text],
    )
    return resp.data[0].embedding

