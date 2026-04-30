from fastapi import FastAPI
from app.routers import property

app = FastAPI(title="Compliance Photo Gallery")

app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Compliance Photo Gallery API"}
