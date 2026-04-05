from typing import List

from pydantic import BaseModel, Field


class Region(BaseModel):
    name: str
    demand: float
    supply: float


class Observation(BaseModel):
    regions: List[Region]
    total_supply: float
    renewable_supply: float
    time_step: int


class Action(BaseModel):
    allocations: List[float] = Field(..., min_length=3, max_length=3)


class Reward(BaseModel):
    value: float

