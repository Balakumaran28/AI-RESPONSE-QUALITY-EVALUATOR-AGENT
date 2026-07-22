from pydantic import BaseModel, Field
from typing import Optional, List
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