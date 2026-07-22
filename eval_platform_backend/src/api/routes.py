from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.api.schemas import EvaluationPayload, EvaluationBatchRequest, EvaluationRequest, EvaluationResponse
from typing import List
from uuid import uuid4
from pydantic import BaseModel
from src.agents.eval_agents import accuracy_judge_agent, hallucination_detection_agent, relevance_judge_agent
from src.rag.vector_store import query_reference_knowledge

app = FastAPI(
    title="LLM Evaluation Platform - Input Module Gateway",
    version="1.0.0",
    description="Module 1: Ingestion entry point handling Single and Batch evaluations."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query_text: str

@app.post("/api/v1/rag/search", status_code=status.HTTP_200_OK)
async def search_vector_store(payload: SearchRequest):
    if not payload.query_text.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    try:
        search_results = query_reference_knowledge(query_text=payload.query_text, top_k=1)
        retrieved_context = search_results['documents'][0][0]
        return {
            "status": "success",
            "query": payload.query_text,
            "retrieved_context": retrieved_context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/evaluate", status_code=status.HTTP_200_OK, response_model=EvaluationResponse)
async def evaluate_response(payload: EvaluationRequest):
    if not payload.question.strip() or not payload.response.strip():
        raise HTTPException(status_code=400, detail="Question and response cannot be empty.")

    try:
        context_chunks = [chunk.strip() for chunk in payload.retrieved_contexts if chunk.strip()]
        if not context_chunks:
            search_results = query_reference_knowledge(query_text=payload.question, top_k=3)
            documents = search_results.get("documents", []) if isinstance(search_results, dict) else []
            for document_group in documents:
                for chunk in document_group:
                    if chunk and chunk.strip():
                        context_chunks.append(chunk.strip())

        relevance = await relevance_judge_agent(payload.question, payload.response)
        accuracy = await accuracy_judge_agent(context_chunks, payload.response, payload.question)
        hallucination = await hallucination_detection_agent(context_chunks, payload.response, payload.question)

        return EvaluationResponse(
            retrieved_contexts=context_chunks,
            relevance=relevance.model_dump(),
            accuracy=accuracy.model_dump(),
            hallucination=hallucination.model_dump(),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/api/v1/evaluate/single", status_code=status.HTTP_202_ACCEPTED)
async def submit_single_evaluation(payload: EvaluationPayload):
    return {
        "status": "success",
        "message": "Single evaluation target successfully verified and queued.",
        "data": payload
    }

@app.post("/api/v1/evaluate/batch", status_code=status.HTTP_202_ACCEPTED)
async def submit_batch_evaluation(payload: EvaluationBatchRequest):
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
