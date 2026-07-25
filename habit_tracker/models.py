from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    id: Optional[int]
    name: str
    description: Optional[str]
    created_at: str
    last_completed: Optional[str]
    streak: int
