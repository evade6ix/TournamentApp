from fastapi import FastAPI
from routers.user_router import router as user_router
from routers.tournament_router import router as tournament_router
from routers.match_router import router as match_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Beyblade X Tournament API",
    description="Backend for user registration, ELO, tournaments and rankings.",
    version="1.0.0"
)

# Register routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(tournament_router, prefix="/tournaments", tags=["Tournaments"])
app.include_router(match_router, prefix="/matches", tags=["Matches"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"msg": "Welcome to the Beyblade X Tournament API!"}

# This runs the app on Railway's assigned port (e.g., 8080)
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
