from app.embedding_service import generate_embedding
from app.vector_store import search_documents
from app.graph_service import driver
from app.llm_service import extract_entities_from_text


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

def answer_question(query):
    vector_results = retrival_service(query, 3)
    vector_context = vector_results["documents"][0]
    sources = []

    for metadata in vector_results["metadatas"][0]:
        source = metadata["source"]
        if source not in sources:
            sources.append(source)



    graph_context = []
    entities = extract_entities_from_text(query)

    for entity in entities:
        results = graph_retrival(entity)
        formatted_results = formatted_graph_output(results)
        for record in formatted_results:
            graph_context.append(record)

    prompt = f"""
    Answer the user's question using the provided Vector Context and Graph Context.

    Question:
    {query}

    Vector Context:
    {vector_context}

    Graph Context:
    {graph_context}


    Use only the information provided in these contexts.
    If the answer is not supported by the contexts, say that the information is not available.
    """

    from app.llm_service import client
    import os

    response = client.chat.completions.create(
        model=os.getenv("TEXT_MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    if answer.strip().lower() == "the information is not available.":
        return{
            "Answer":answer,
            "Sources":"No Source Available",
            "Graph": "No Graph Context"
        }
    else:
        return{
                "Answer":answer,
                "Sources":sources,
                "Graph": graph_context}