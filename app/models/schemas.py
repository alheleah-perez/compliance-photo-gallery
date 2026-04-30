from pydantic import BaseModel

class PropertyBase(BaseModel):
    address: str
    realtor_id: int
    price: float

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int

    class Config:
        from_attributes = True
