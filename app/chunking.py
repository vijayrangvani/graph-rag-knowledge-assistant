def chunk_text(text, chunk_size=1000,overlap=200):
    """
    Splits the input text into chunks of specified size with optional overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The size of each chunk. Default is 1000 characters.
        overlap (int): The number of overlapping characters between chunks. Default is 200 characters.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # Move the start index forward by chunk_size minus overlap
    return chunks   