from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput
from ai_profiling.datatypes.planning_datatype import (
    JsonTranslationStatModel,
    SimplePlanningModel,
)
from ai_profiling.helpers.service_helper.language_model_service_datatype import (
    LlmResponse,
)
from nl2flow.debug.schemas import Report


class TemporalFailureModel(str, Enum):
    JSON_PARSING = "JSON_PARSING"
    CLASSICAL_PLANNING = "CLASSICAL_PLANNING"


class LLMResponsePlanningData(BaseModel):
    planning_prompt: str
    llm_response: LlmResponse
    pddl_generator_output: PddlGeneratorOutput
    is_concise: bool = False


class ValOutputModel(BaseModel):
    is_optimal: bool = False
    is_valid: bool = False
    is_executable: bool = False
    reach_goals: bool = False
    cost: int = -1
    output_txt: str = ""
    error_message: str = ""


class ValidationLLMResponsePlanningData(BaseModel):
    llm_response_planning_data: Optional[LLMResponsePlanningData] = None
    llm_plan: Optional[List[str]] = None
    report_soundness: Optional[Report] = None
    report_validity: Optional[Report] = None
    report_optimality: Optional[Report] = None
    val_output_model: Optional[ValOutputModel] = None


class ValidationLLMResponseJsonData(BaseModel):
    llm_response_planning_data: Optional[LLMResponsePlanningData] = None
    planning_input_from_llm: Optional[SimplePlanningModel] = None
    json_translation_stat: Optional[JsonTranslationStatModel] = None
    temporal_failure: Optional[TemporalFailureModel] = None
    error_messages: List[str] = []

    def update_error_message(self, message: str) -> None:
        if len(message) > 0:
            self.error_messages.append(message[:])
