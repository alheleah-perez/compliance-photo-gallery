from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Realtor(Base):
    __tablename__ = "realtors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    properties = relationship("Property", back_populates="realtor")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    price = Column(Float)
    realtor_id = Column(Integer, ForeignKey("realtors.id"))

    realtor = relationship("Realtor", back_populates="properties")
    image_pairs = relationship("ImagePair", back_populates="property")

class ImagePair(Base):
    __tablename__ = "image_pairs"

    id = Column(Integer, primary_key=True, index=True)
    compliance_id = Column(String, unique=True, index=True)
    original_url = Column(String)
    edited_url = Column(String)
    edit_description = Column(String)
    compliance_note = Column(String)
    property_id = Column(Integer, ForeignKey("properties.id"))

    property = relationship("Property", back_populates="image_pairs")
