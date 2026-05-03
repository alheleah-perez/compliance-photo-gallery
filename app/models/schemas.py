from pydantic import BaseModel, HttpUrl

class PropertyBase(BaseModel):
    address: str
    realtor_id: int
    price: float

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    disclosure_status: bool = False

    class Config:
        from_attributes = True

class ImagePair(BaseModel):
    original_url: HttpUrl
    edited_url: HttpUrl
    edit_description: str

class ImagePairResponse(BaseModel):
    compliance_id: str
    property_id: int
    original_url: HttpUrl
    edited_url: HttpUrl
    edit_description: str
    compliance_note: str
