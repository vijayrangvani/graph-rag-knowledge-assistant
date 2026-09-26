from app.embedding_service import generate_embedding
from app.vector_store import search_documents
from app.graph_service import driver

def retrival_service(query: str,k: int):
    """
    Retrieval service function that handles the retrieval of data from a specified source
    Take query as input and convert it into an embedding using the generate_embedding function
    Then use the embedding to retrieve relevant data from the ChromaDb and also have the same from Graph Db 
    """
    query_embedding = generate_embedding(query)
    results = search_documents(query_embedding,k)
    return results 

def graph_retrival(entity_name):
    with driver.session() as session:
        results =session.run("""
            MATCH (a:Entity {name: $entity_name})-[r]->(b)
            RETURN a, r, b """,
            entity_name=entity_name)
        records = list(results)
    return records

def formatted_graph_output(results):
    formatted_results = []
    for record in results:
        source = record["a"]["name"]
        relationship = record["r"].type
        target = record["b"]["name"]
        formatted_results.append(f"{source} -[{relationship}]-> {target}")   
    return formatted_results