# pip install openai
import os
from unittest import result
from urllib import response
from openai import OpenAI
from dotenv import load_dotenv
from .graph_service import create_relationship

import json 

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

SYSTEM_PROMPT = """
You are  expert assistant who understands text.
Give me output as entity and relationship.Strictly in JSON format 

EXAMPLE 

Q: Neo4j is a graph database used by developers to store connected data.
A: {
  "entities": [
    "Neo4j",
    "Graph Database",
    "Developers",
    "Connected Data"
  ],
  "relationships": [
    {
      "source": "Neo4j",
      "type": "IS_A",
      "target": "Graph Database"
    }
  ]
}

"""


def get_entity_relationship(user_query): 

    response = client.chat.completions.create(
        model=os.getenv("TEXT_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
        temperature=0.7,
    )
    results = json.loads(response.choices[0].message.content)
    for relationship in results.get("relationships", []):
        source = relationship.get("source")
        target = relationship.get("target")
        rel_type = relationship.get("type")
        create_relationship(source, target, rel_type)    

    return results  #return source, relationship, target in JSON format


