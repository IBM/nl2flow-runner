from typing import List, Optional
from pydantic import BaseModel


class LlmRecord(BaseModel):
    prompts: List[str]
    responses: List[str]
    prompt_source_hash: str
    model_name: str
    model_temperature: float
    service_lag_millisecond: float
    error_message: Optional[str]
    token_length_prompts: Optional[int]
    token_length_responses: Optional[int]
