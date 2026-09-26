from app.pdf_service import extract_text
from app.chunking import chunk_text
from app.embedding_service import generate_embedding
from app.vector_store import add_documents
from app.llm_service import get_entity_relationship


def ingest_document(file_path):
    extracted_text = extract_text(file_path)
    chunks = chunk_text(extracted_text)
    embeddings = [generate_embedding(chunk) for chunk in chunks]
    add_documents(chunks, embeddings, file_path.name)
    for chunk in chunks:
        get_entity_relationship(chunk)
