from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.routers import property
from app import crud, auth, models
from app.database import get_db, engine
from app.models import orm_models, schemas

orm_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Compliance Photo Gallery")

app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Compliance Photo Gallery API"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/compliance-check/{property_id}")
def compliance_check(property_id: int, db: Session = Depends(get_db)):
    image_pairs = crud.get_image_pairs_by_property(db=db, property_id=property_id)
    return {"property_id": property_id, "edits": image_pairs}
