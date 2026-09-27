# # from app.ingestion_service import ingest_document
# # from pathlib import Path

# # ingest_document(Path("data/Upgrade_Tool_Troubleshooting_Guide.pdf"))
# # ingest_document(Path("data/Upgrade_Tool_Support_Knowledge_Base.pdf"))

# # # print("Both documents ingested")

# from app.retrival_service import retrival_service,graph_retrival,formatted_graph_output
# from app.llm_service import extract_entities_from_text
# query = "What should be done if the issue is database error?"
# vector_results = retrival_service(query, 1)
# vector_context = vector_results["documents"][0]
# sources = []

# for metadata in vector_results["metadatas"][0]:
#     source = metadata["source"]
#     if source not in sources:
#         sources.append(source)



# graph_context = []
# entities = extract_entities_from_text(query)

# for entity in entities:
#     results = graph_retrival(entity)
#     formatted_results = formatted_graph_output(results)
#     for record in formatted_results:
#         graph_context.append(record)

# prompt = f"""
# Answer the user's question using the provided Vector Context and Graph Context.

# Question:
# {query}

# Vector Context:
# {vector_context}

# Graph Context:
# {graph_context}


# Use only the information provided in these contexts.
# If the answer is not supported by the contexts, say that the information is not available.
# """

# from app.llm_service import client
# import os

# response = client.chat.completions.create(
#     model=os.getenv("TEXT_MODEL"),
#     messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ],
#     temperature=0.2
# )

# answer = response.choices[0].message.content

# if answer.strip().lower() == "the information is not available.":
#     print("\nFinal Answer:")
#     print(answer)
# else:
#     print("\nFinal Answer:")
#     print(answer)

#     print("\nSources:")
#     for source in sources:
#         print(source)

import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("documents")

print("Total chunks:", collection.count())

data = collection.get(include=["metadatas"])

for metadata in data["metadatas"]:
    print(metadata)

from app.graph_service import driver

with driver.session() as session:
    result = session.run("""
        MATCH (n:Entity)
        RETURN n.name AS entity
        ORDER BY entity
    """)

    for record in result:
        print(record["entity"])

driver.close()