from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Tournament(BaseModel):
    name: str
    description: Optional[str] = ""
    organizer_id: str  # Admin user ID
    event_date: datetime

    players: List[str] = Field(default_factory=list)  # List of user emails or IDs
    status: str = "upcoming"  # upcoming, ongoing, completed

    created_at: datetime = Field(default_factory=datetime.utcnow)
