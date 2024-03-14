from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_redirect_root_to_docs():
    response = client.get("/")
    assert response.status_code == 200

def test_bugsGetAll():
    response = client.get("/bugs/list/all")
    assert response.status_code == 200
    assert response.json() == {"success": "[(6, 3, 2, 'black screen fix pls', 'open'), (7, 2, 3, 'font CRASH', 'open'), (8, 1, 1, 'bold text lag', 'fixed'), (9, 1, 3, 'testadd asldkfa;sld', 'open'), (11, 2, 2, '2', '2'), (14, 1, 1, 'asdf1234', 'open')]"}

def test_bugsGetApp():
    response = client.get("/bugs/list/app?appid=1")
    assert response.status_code == 200
    assert response.json() == {"success": "[(8, 1, 1, 'bold text lag', 'fixed'), (9, 1, 3, 'testadd asldkfa;sld', 'open'), (14, 1, 1, 'asdf1234', 'open')]"}

def test_bugsGetOpen():
    response = client.get("/bugs/list/open")
    assert response.status_code == 200
    assert response.json() == {"success": "[(6, 3, 2, 'black screen fix pls', 'open'), (7, 2, 3, 'font CRASH', 'open'), (9, 1, 3, 'testadd asldkfa;sld', 'open'), (14, 1, 1, 'asdf1234', 'open')]"}

def test_bugsGetFixed():
    response = client.get("/bugs/list/fixed")
    assert response.status_code == 200
    assert response.json() == {"success": "[(8, 1, 1, 'bold text lag', 'fixed')]"}

def test_ping():
    response = client.get("/connection/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_login():
    response = client.post("/users/login", data={"name":"komissarov","password":"password"})
    assert response.status_code == 200
    assert response.json() == {
  "status": [
    1,
    "admin"
  ]
}

def test_register():
    response = client.post("/users/register", data={"name":"komissarov","password":"pass", "access":"admin"})
    assert response.status_code == 200
    assert response.json() == {
  "status": "already exists"
}

def test_addBug():
    response = client.post("/bugs/add", data={"appid":1, "authorid":1, "title":"1", "status":"open"})
    assert response.status_code == 200
    assert response.json() == {
  "status": "success"
}

def test_editBug():
    response = client.post("/bugs/edit", data={"id":20, "appid":2, "authorid":2, "title":"2", "status":"fixed"})
    assert response.status_code == 200
    assert response.json() == {
  "status": "success"
}

def test_deleteBug():
    response = client.post("/bugs/delete", data={"id":20})
    assert response.status_code == 200
    assert response.json() == {
  "status": "success"
}