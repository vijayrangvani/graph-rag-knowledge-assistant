from app.ingestion_service import ingest_document
from app.vector_store import search_documents
from app.embedding_service import generate_embedding

# ingest_document("data/pdf-test.pdf")
# print("Success..")

query = "how are PDF forms indicated?"

embedings = generate_embedding(query)

results = search_documents(embedings,3)
print(results["documents"])