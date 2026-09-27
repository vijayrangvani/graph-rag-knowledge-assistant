from fastapi import FastAPI,File,UploadFile,HTTPException
from pathlib import Path
from app.pdf_service import extract_text 
from app.ingestion_service import ingest_document
from pydantic import BaseModel
from app.retrival_service import answer_question
from app.graph_service import get_graph

class QuestionRequest(BaseModel):
    question: str

app = FastAPI(title="GraphRAG Application",
              version="1.0")

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_PDF(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = data_dir/file.filename

    with open(file_path,"wb") as f:
        f.write(await file.read())

    ingest_document(file_path)

    return {
        "filename":file.filename,
        "message":"File uploaded & Ingested Successfully.."

    }

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    result = answer_question(request.question)
    return result

@app.get("/graph")
async def graph():
    return get_graph()

@app.get("/extract/{file_name}")
def extract(file_name: str):
    file_path = data_dir/file_name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    text = extract_text(file_path)
    return {
        "characters":len(text),
        "extracted_text":text[:1000]  # Return first 1000 characters of the extracted text      
    }   