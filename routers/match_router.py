from fastapi import APIRouter, HTTPException, Depends
from db.mongo import db
from auth.auth import decode_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from models.match import Match
from utils.elo import calculate_elo
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Authenticated user helper
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

# ✅ Submit match result
@router.post("/submit")
async def submit_match_result(match: Match, current_user: dict = Depends(get_current_user)):
    if current_user["email"] not in [match.player1_id, match.player2_id]:
        raise HTTPException(status_code=403, detail="You’re not part of this match.")

    if not match.winner_id:
        raise HTTPException(status_code=400, detail="Winner ID required")

    # Fetch both players
    p1 = await db.users.find_one({"email": match.player1_id})
    p2 = await db.users.find_one({"email": match.player2_id})
    if not p1 or not p2:
        raise HTTPException(status_code=404, detail="Player not found")

    # Calculate new ELOs
    new_p1_elo, new_p2_elo = calculate_elo(
        p1["elo"], p2["elo"], winner=match.winner_id
    )

    # Update match record
    match.player1_elo_after = new_p1_elo
    match.player2_elo_after = new_p2_elo
    match.reported_by = current_user["email"]
    match.reported_at = datetime.utcnow()
    await db.matches.insert_one(match.dict())

    # Update players
    p1_result = "win" if match.winner_id == match.player1_id else "loss"
    p2_result = "win" if match.winner_id == match.player2_id else "loss"

    await db.users.update_one(
        {"email": match.player1_id},
        {
            "$set": {"elo": new_p1_elo},
            "$inc": {"wins": 1 if p1_result == "win" else 0, "losses": 1 if p1_result == "loss" else 0},
            "$push": {"match_history": {
                "opponent": match.player2_id,
                "result": p1_result,
                "elo_change": new_p1_elo - p1["elo"],
                "timestamp": datetime.utcnow()
            }}
        }
    )

    await db.users.update_one(
        {"email": match.player2_id},
        {
            "$set": {"elo": new_p2_elo},
            "$inc": {"wins": 1 if p2_result == "win" else 0, "losses": 1 if p2_result == "loss" else 0},
            "$push": {"match_history": {
                "opponent": match.player1_id,
                "result": p2_result,
                "elo_change": new_p2_elo - p2["elo"],
                "timestamp": datetime.utcnow()
            }}
        }
    )

    return {"msg": "Match result recorded and ELO updated."}
