from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers import property
from app import crud
from app.database import get_db, engine
from app.models import orm_models

orm_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Compliance Photo Gallery")

app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Compliance Photo Gallery API"}

@app.get("/compliance-check/{property_id}")
def compliance_check(property_id: int, db: Session = Depends(get_db)):
    image_pairs = crud.get_image_pairs_by_property(db=db, property_id=property_id)
    return {"property_id": property_id, "edits": image_pairs}
