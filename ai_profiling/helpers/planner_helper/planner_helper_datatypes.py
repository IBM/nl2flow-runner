from typing import Optional
from pydantic import BaseModel


class PlanQuality(BaseModel):
    is_optimal_plan: Optional[bool]
    is_executable_plan: Optional[bool]
    is_valid_plan: Optional[bool]
