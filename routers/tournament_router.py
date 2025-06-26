from fastapi import APIRouter, HTTPException, Depends
from models.tournament import Tournament
from db.mongo import db
from auth.auth import decode_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# ✅ Get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

# ✅ Create Tournament (Admin only)
@router.post("/create")
async def create_tournament(tournament: Tournament, current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Only admins can create tournaments")
    
    tournament.organizer_id = current_user["_id"]
    await db.tournaments.insert_one(tournament.dict())
    return {"msg": "Tournament created successfully"}

# 🌐 Get all tournaments
@router.get("/all", response_model=List[dict])
async def get_all_tournaments():
    tournaments = await db.tournaments.find().to_list(length=100)
    for t in tournaments:
        t["_id"] = str(t["_id"])  # Convert ObjectId to string for JSON
    return tournaments

# 🙋 Register for a tournament
@router.post("/register/{tournament_id}")
async def register_for_tournament(tournament_id: str, current_user: dict = Depends(get_current_user)):
    tournament = await db.tournaments.find_one({"_id": tournament_id})
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    if current_user["email"] in tournament.get("players", []):
        raise HTTPException(status_code=400, detail="Already registered")

    await db.tournaments.update_one(
        {"_id": tournament_id},
        {"$push": {"players": current_user["email"]}}
    )
    return {"msg": "Registered for tournament"}
