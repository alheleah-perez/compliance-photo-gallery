import uuid
from fastapi import APIRouter, HTTPException
from app.models.schemas import Property, PropertyCreate, ImagePair, ImagePairResponse

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

# Dummy database
dummy_properties = {
    1: {"id": 1, "address": "123 Main St", "realtor_id": 101, "price": 500000.0},
    2: {"id": 2, "address": "456 Oak Ave", "realtor_id": 102, "price": 750000.0}
}

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int):
    # Returning dummy data for now
    if property_id in dummy_properties:
        return dummy_properties[property_id]
    return {"id": property_id, "address": "Not Found", "realtor_id": 0, "price": 0.0}

@router.post("/", response_model=Property)
def create_property(property: PropertyCreate):
    new_id = max(dummy_properties.keys()) + 1 if dummy_properties else 1
    new_property = Property(id=new_id, **property.model_dump())
    dummy_properties[new_id] = new_property.model_dump()
    return new_property

@router.post("/{property_id}/upload-pair", response_model=ImagePairResponse)
def upload_image_pair(property_id: int, image_pair: ImagePair):
    if property_id not in dummy_properties:
        raise HTTPException(status_code=404, detail="Property not found")
    
    compliance_id = str(uuid.uuid4())
    
    # Referencing the project mission for California AB 723 transparency requirements
    compliance_note = (
        "California AB 723 Compliance: "
        "Digitally altered images that materially change the property's appearance "
        "must be conspicuously labeled. The original, unaltered image must also be provided "
        "in the same advertisement."
    )
    
    return ImagePairResponse(
        compliance_id=compliance_id,
        property_id=property_id,
        original_url=image_pair.original_url,
        edited_url=image_pair.edited_url,
        edit_description=image_pair.edit_description,
        compliance_note=compliance_note
    )
