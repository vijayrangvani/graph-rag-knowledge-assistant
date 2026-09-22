from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# 1. Database Configuration
URI = os.getenv("NEO4J_URI")
AUTH = ("neo4j", os.getenv('NEO4J_PASSWORD'))

# 2. Initialize the Neo4j Driver
driver = GraphDatabase.driver(URI, auth=AUTH)

# #3. Open connection and Write a query to the database
# with driver.session() as session:
#         message = session.run("RETURN 'Welcome to Graph 4j'").single()
#         print(message)

# #4. Close the connection
# driver.close()

def create_relationship(source,target,relationship):
    with driver.session() as session:
        session.run(
                "MERGE (a:Entity {name: $source}) "
                "MERGE (b:Entity {name: $target}) "
                "MERGE (a)-[:$($relationship)]->(b)",
                source=source, target=target, relationship=relationship
                )   


