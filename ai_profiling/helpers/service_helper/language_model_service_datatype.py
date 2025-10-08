from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class LlmResponse(BaseModel):
    llm_model_id: str
    generated_text: str = ""
    perplexity: Optional[float] = float("inf")
    error_messages: List[str] = []
    lag: float  # millisecond


class UnifiedModelClassificationType(str, Enum):
    SINGLE = "single"
    SEQUENCE = "sequence"
    CLARIFICATION = "clarify"


class UnifiedModelResponseModel(BaseModel):
    type: UnifiedModelClassificationType = UnifiedModelClassificationType.CLARIFICATION
    intents: List[str] = []
    clarification_question: str = ""
    error_messages: List[str] = []


LLM_SERVICE_BASE_URL: str = ""
LLM_SERVICE_COMPLETION_RESOURCE: str = "v1/completions"
MODEL_ID_RESOURCE_DICT_BASE = {
    "mistralai/mixtral-8x22B-instruct-v0.1": "mixtral-8x22b-instruct-v01",
    "meta-llama/llama-3-3-70b-instruct": "llama-3-3-70b-instruct",
    "Qwen/Qwen2.5-72B-Instruct": "qwen2-5-72b-instruct",
    "ibm-granite/granite-3.3-8b-instruct": "granite-3-3-8b-instruct",
    "deepseek-ai/DeepSeek-V3": "deepseek-v3-h200",
    "meta-llama/Llama-3.1-8B-Instruct": "llama-3-1-8b-instruct",
    "meta-llama/llama-3-1-405b-instruct-fp8": "llama-3-1-405b-instruct-fp8",
    "deepseek-ai/deepseek-coder-33b-instruct": "deepseek-coder-33b-instruct",
    "codellama/CodeLlama-34b-Instruct-hf": "codellama-34b-instruct-hf",
}
MODEL_ID_RESOURCE_DICT: Dict[str, str] = {k.lower(): v for k, v in MODEL_ID_RESOURCE_DICT_BASE.items()}
