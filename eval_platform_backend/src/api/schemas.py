from pydantic import AliasChoices, BaseModel, Field
from typing import Any, Optional, List
from uuid import UUID, uuid4
from datetime import datetime

class EvaluationPayload(BaseModel):
    """Fulfills the Input Gateway validation schema contract for a single transaction."""
    question_text: str = Field(
        ..., 
        min_length=5, 
        description="The raw string containing the user's initial prompt or query."
    )
    ai_response_text: str = Field(
        ..., 
        min_length=1, 
        description="The generated text output being scrutinized for errors."
    )
    reference_answer_text: Optional[str] = Field(
        None, 
        description="Optional master-key text containing the human ground-truth."
    )
    source_document_text: Optional[str] = Field(
        None, 
        description="Optional context payload uploaded directly by the user."
    )

class EvaluationBatchRequest(BaseModel):
    """Fulfills the transactional bulk batch request architecture schema."""
    job_id: UUID = Field(default_factory=uuid4, description="Unique transactional session tracking identifier.")
    dataset_name: str = Field(default="Custom Upload", description="The catalog tag marking the testing suite.")
    test_cases: List[EvaluationPayload] = Field(..., description="Array of individual evaluation items.")


class EvaluationRequest(BaseModel):
    """Network schema for a single evaluation request submitted by the frontend."""
    question: str = Field(..., min_length=1, description="The user question to evaluate")
    response: str = Field(..., min_length=1, description="The response that should be judged")
    retrieved_contexts: List[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices(
            "retrieved_contexts", "rag_retrieved_answers", "rag_retrieved_semantic_answers"
        ),
        description="Optional RAG chunks/semantic answers used as the sole grounding evidence.",
    )


class EvaluationResponse(BaseModel):
    """Structured response container for the RAG evidence and evaluation results."""
    retrieved_contexts: List[str] = Field(
        default_factory=list,
        description="RAG chunks used as grounding evidence for accuracy and hallucination scoring.",
    )
    relevance: dict[str, Any] = Field(..., description="Relevance evaluation payload")
    accuracy: dict[str, Any] = Field(..., description="Accuracy evaluation payload")
    hallucination: dict[str, Any] = Field(..., description="Hallucination evaluation payload")
