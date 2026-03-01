from typing import List, Optional
from pydantic import BaseModel


class FdcCandidate(BaseModel):
    fdc_id: int
    description: str
    dataType: Optional[str] = None


class ConfirmItem(BaseModel):
    item_id: str
    fdc_id: int
    grams_final: float


class ConfirmRequest(BaseModel):
    meal_id: str
    items: List[ConfirmItem]
