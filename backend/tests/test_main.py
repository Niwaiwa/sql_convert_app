from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "sql convert tool backend started."}

    
def test_sql():
    response = client.post("/sql", json={"sql": "select * from table1"})
    assert response.status_code == 200
    assert response.json() == {"sql": "select * from table1"}


def test_sql_with_empty_sql():
    response = client.post("/sql", json={"sql": ""})
    assert response.status_code == 200
    assert response.json() == {"sql": ""}


def test_get_sql(): 
    response = client.get("/sql")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["page"] == 1
    assert response_data["limit"] == 10


def test_get_sql_with_limit_offset_order_by():
    response = client.get("/sql?limit=1&offset=0&order_by=id")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["page"] == 1
    assert response_data["limit"] == 1
    assert 1 == len(response_data["data"])


if __name__ == "__main__":
    # import pytest
    # pytest.main(["-s", "test_main.py"])
    print("test_main.py")