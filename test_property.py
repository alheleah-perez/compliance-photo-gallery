from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_image_pairs():
    from app.database import SessionLocal, engine
    from app.models import orm_models
    
    db = SessionLocal()
    orm_models.Base.metadata.create_all(bind=engine)
    
    realtor = orm_models.Realtor(name="Test Realtor")
    db.add(realtor)
    db.commit()
    db.refresh(realtor)
    
    response = client.post(
        "/properties/",
        json={"address": "123 Test St", "realtor_id": realtor.id, "price": 100000.0}
    )
    assert response.status_code == 200
    property_id = response.json()["id"]
    
    pair1 = {
        "original_url": "http://example.com/orig1.jpg",
        "edited_url": "http://example.com/edit1.jpg",
        "edit_description": "Added virtual furniture"
    }
    resp1 = client.post(f"/properties/{property_id}/upload-pair", json=pair1)
    assert resp1.status_code == 200
    
    pair2 = {
        "original_url": "http://example.com/orig2.jpg",
        "edited_url": "http://example.com/edit2.jpg",
        "edit_description": "Removed trash can"
    }
    resp2 = client.post(f"/properties/{property_id}/upload-pair", json=pair2)
    assert resp2.status_code == 200
    
    check_response = client.get(f"/compliance-check/{property_id}")
    assert check_response.status_code == 200
    data = check_response.json()
    
    assert len(data["edits"]) == 2
    assert data["edits"][0]["edit_description"] == "Added virtual furniture"
    assert data["edits"][1]["edit_description"] == "Removed trash can"
    
    db.close()
