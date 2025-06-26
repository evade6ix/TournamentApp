from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Match(BaseModel):
    tournament_id: str  # ID of the tournament
    round: int           # Round number
    player1_id: str      # User ID or email
    player2_id: str
    winner_id: Optional[str] = None  # Set after result is submitted

    player1_elo_before: int
    player2_elo_before: int
    player1_elo_after: Optional[int] = None
    player2_elo_after: Optional[int] = None

    reported_by: Optional[str] = None  # Who submitted the result
    reported_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
