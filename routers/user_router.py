from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.user import User
from db.mongo import db
from auth.auth import hash_password, verify_password, create_access_token, decode_token
from jose import JWTError
from typing import Optional
import uuid
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
AVATAR_UPLOAD_DIR = "static/avatars"

class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ Register
@router.post("/register")
async def register_user(user: User):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = hash_password(user.password)
    await db.users.insert_one(user.dict())
    return {"msg": "User registered successfully"}

# ✅ Login
@router.post("/login", response_model=Token)
async def login_user(form: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form.username})
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

# ✅ Get current user
@router.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.pop("password")
        user["is_admin"] = user.get("is_admin", False)
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

# 🏆 Leaderboard
@router.get("/leaderboard")
async def leaderboard(limit: int = 50):
    users = await db.users.find().sort("elo", -1).limit(limit).to_list(length=limit)

    result = []
    for user in users:
        result.append({
            "username": user.get("username"),
            "profile_picture": user.get("profile_picture"),
            "elo": user.get("elo"),
            "wins": user.get("wins", 0),
            "losses": user.get("losses", 0),
            "rank": user.get("rank"),
            "is_admin": user.get("is_admin", False)
        })

    return result

# 📤 Upload Avatar
@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)
        filepath = os.path.join(AVATAR_UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(await file.read())

        avatar_url = f"/static/avatars/{filename}"
        await db.users.update_one({"email": email}, {"$set": {"profile_picture": avatar_url}})
        return {"msg": "Avatar uploaded", "url": avatar_url}

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

# ✏️ Edit user profile
class ProfileEdit(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

@router.put("/edit")
async def edit_profile(data: ProfileEdit, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        updates = {}
        # ✅ Check for username conflict
        if data.username and data.username != user.get("username"):
            if await db.users.find_one({"username": data.username}):
                raise HTTPException(status_code=400, detail="Username already taken.")
            updates["username"] = data.username

        if data.bio is not None:
            updates["bio"] = data.bio
        if data.profile_picture is not None:
            updates["profile_picture"] = data.profile_picture

        if not updates:
            raise HTTPException(status_code=400, detail="No profile fields to update.")

        await db.users.update_one({"email": email}, {"$set": updates})
        return {"msg": "Profile updated successfully."}

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
