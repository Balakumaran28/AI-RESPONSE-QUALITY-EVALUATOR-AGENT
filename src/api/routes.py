from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from src.api.schemas import EvaluationPayload, EvaluationBatchRequest
from typing import List
from uuid import uuid4

app = FastAPI(
    title="LLM Evaluation Platform - Input Module Gateway",
    version="1.0.0",
    description="Module 1: Ingestion entry point handling Single and Batch evaluations."
)

@app.post("/api/v1/evaluate/single", status_code=status.HTTP_202_ACCEPTED)
async def submit_single_evaluation(payload: EvaluationPayload):
    """Accepts a single question-answer target payload and verifies data invariants."""
    return {
        "status": "success",
        "message": "Single evaluation target successfully verified and queued.",
        "data": payload
    }

@app.post("/api/v1/evaluate/batch", status_code=status.HTTP_202_ACCEPTED)
async def submit_batch_evaluation(payload: EvaluationBatchRequest):
    """Processes mass arrays of evaluation targets simultaneously for dataset benchmarks."""
    total_records = len(payload.test_cases)
    if total_records == 0:
        raise HTTPException(status_code=400, detail="Batch array cannot be empty.")
        
    return {
        "status": "success",
        "job_id": payload.job_id,
        "dataset_name": payload.dataset_name,
        "total_records_ingested": total_records,
        "message": f"Successfully validated and initialized batch execution pipeline."
    }

@app.post("/api/v1/evaluate/upload-context")
async def upload_source_document(file: UploadFile = File(...)):
    """Accepts raw reference document text files directly at the gateway layer."""
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only raw text (.txt) files are supported.")
        
    contents = await file.read()
    try:
        decoded_text = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding must be UTF-8.")
        
    return {
        "status": "success",
        "filename": file.filename,
        "file_size_bytes": len(contents),
        "character_count": len(decoded_text),
        "snippet_preview": decoded_text[:150] + "..." if len(decoded_text) > 150 else decoded_text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.routes:app", host="127.0.0.1", port=8000, reload=True)