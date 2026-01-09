from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Sidekick TA")
app.include_router(router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Autonomous TA Server Running"}