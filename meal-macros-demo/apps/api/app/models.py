from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Meal(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    image_path: str
    image_hash: str = Field(index=True, unique=True)
    status: str = Field(default="draft")
    totals_estimated_json: dict = Field(sa_column=Column(JSON))
    totals_final_json: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))


class MealItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    meal_id: str = Field(index=True, foreign_key="meal.id")
    name_guess: str
    fdc_id: Optional[int] = None
    fdc_description: Optional[str] = None
    grams_estimated: float
    grams_final: Optional[float] = None
    portion_multiplier: float = 1.0
    confidence_recognition: float
    confidence_match: float
    confidence_portion: float
    nutrients_estimated_json: dict = Field(sa_column=Column(JSON))
    nutrients_final_json: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
    fdc_candidates_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    per_gram_nutrients_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
