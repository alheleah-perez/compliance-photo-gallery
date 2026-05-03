import uuid
from sqlalchemy.orm import Session
from app.models import orm_models, schemas

def create_property(db: Session, property: schemas.PropertyCreate):
    db_property = orm_models.Property(
        address=property.address,
        price=property.price,
        realtor_id=property.realtor_id,
        disclosure_status=False
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def add_image_pair(db: Session, property_id: int, image_pair: schemas.ImagePair, compliance_note: str):
    db_image_pair = orm_models.ImagePair(
        compliance_id=str(uuid.uuid4()),
        original_url=str(image_pair.original_url),
        edited_url=str(image_pair.edited_url),
        edit_description=image_pair.edit_description,
        compliance_note=compliance_note,
        property_id=property_id
    )
    db.add(db_image_pair)
    db.commit()
    db.refresh(db_image_pair)
    return db_image_pair

def get_image_pairs_by_property(db: Session, property_id: int):
    return db.query(orm_models.ImagePair).filter(orm_models.ImagePair.property_id == property_id).all()

def update_disclosure_status(db: Session, property_id: int, status: bool):
    db_property = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if db_property:
        db_property.disclosure_status = status
        db.commit()
        db.refresh(db_property)
    return db_property

def get_user_by_username(db: Session, username: str):
    return db.query(orm_models.Realtor).filter(orm_models.Realtor.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    from app import auth
    hashed_password = auth.get_password_hash(user.password)
    db_user = orm_models.Realtor(
        username=user.username,
        hashed_password=hashed_password,
        realtor_license_number=user.realtor_license_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

