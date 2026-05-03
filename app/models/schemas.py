from pydantic import BaseModel, HttpUrl

class PropertyBase(BaseModel):
    address: str
    price: float
    realtor_id: Optional[int] = None

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

class UserBase(BaseModel):
    username: str
    realtor_license_number: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    name: Optional[str] = None

    class Config:
        from_attributes = True

