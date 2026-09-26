import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")

def add_documents(chunks, embeddings, file_name):

    ids = [f"{file_name}_{i}"
        for i in range(len(chunks))
    ]   

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )


def search_documents(embeddings,k=3):
    results = collection.query(
        query_embeddings=embeddings,
        n_results=k
    )
    return results