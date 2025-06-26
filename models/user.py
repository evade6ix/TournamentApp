from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # Hashed
    profile_picture: Optional[str] = None
    bio: Optional[str] = ""

    # Game stats
    elo: int = 1000
    wins: int = 0
    losses: int = 0
    rank: Dict[str, str] = Field(default_factory=lambda: {"tier": "Bronze", "division": "III"})
    match_history: List[Dict] = Field(default_factory=list)

    # Permissions
    is_admin: bool = False

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
