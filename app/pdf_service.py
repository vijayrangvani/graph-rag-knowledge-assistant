from pypdf import PdfReader

def extract_text(file_name):
    """
    Extracts text from a PDF file.

    Args:
        file_name (str): The name of the PDF file.  

    Returns:
        str: The extracted text from the PDF file.
    """
    text = ""
    with open(file_name, "rb") as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text()
    return text 