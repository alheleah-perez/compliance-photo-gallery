from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import Property, PropertyCreate, ImagePair, ImagePairResponse
from app import crud
from app.database import get_db

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    from app.models import orm_models
    db_property = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@router.post("/", response_model=Property)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    return crud.create_property(db=db, property=property)

@router.post("/{property_id}/upload-pair", response_model=ImagePairResponse)
def upload_image_pair(property_id: int, image_pair: ImagePair, db: Session = Depends(get_db)):
    from app.models import orm_models
    db_property = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    compliance_id = str(uuid.uuid4())
    
    # Referencing the project mission for California AB 723 transparency requirements
    compliance_note = (
        "California AB 723 Compliance: "
        "Digitally altered images that materially change the property's appearance "
        "must be conspicuously labeled. The original, unaltered image must also be provided "
        "in the same advertisement."
    )
    
    return crud.add_image_pair(db=db, property_id=property_id, image_pair=image_pair, compliance_note=compliance_note)
