from models.manufacturer import ManufacturerModel
from test.test_fixtures import *


@pytest.fixture()
async def manufacturers_entry(client: AsyncClient) -> ManufacturerModel:
    response = await client.post("/manufacturers", json={"name": "VAZ", "country": "Russia"})
    body = response.json()

    assert response.status_code == 200
    assert body["name"] == "VAZ"
    assert body["country"] == "Russia"

    return body


async def test_list_manufacturers(client: AsyncClient, manufacturers_entry: ManufacturerModel):
    response = await client.get("/manufacturers")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["id"] == manufacturers_entry["id"]
    assert body[0]["name"] == manufacturers_entry["name"]
    assert body[0]["country"] == manufacturers_entry["country"]


async def test_get_manufacturers(client: AsyncClient, manufacturers_entry: ManufacturerModel):
    response = await client.get(f"/manufacturers/{manufacturers_entry['id']}")
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == manufacturers_entry["id"]
    assert body["name"] == manufacturers_entry["name"]
    assert body["country"] == manufacturers_entry["country"]


async def test_patch_manufacturers(client: AsyncClient, manufacturers_entry: ManufacturerModel):
    response = await client.patch(f"/manufacturers/{manufacturers_entry['id']}", json={"name": "UAZ"})
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == manufacturers_entry["id"]
    assert body["name"] == "UAZ"
    assert body["country"] == manufacturers_entry["country"]


async def test_override_manufacturers(client: AsyncClient, manufacturers_entry: ManufacturerModel):
    response = await client.patch(f"/manufacturers/{manufacturers_entry['id']}", json={
        "name": "KIA",
        "country": "Korea"
    })
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == manufacturers_entry["id"]
    assert body["name"] == "KIA"
    assert body["country"] == "Korea"


async def test_delete_manufacturers(client: AsyncClient, manufacturers_entry: ManufacturerModel):
    response = await client.get(f"/manufacturers/{manufacturers_entry['id']}")
    assert response.status_code == 200

    response = await client.delete(f"/manufacturers/{manufacturers_entry['id']}")
    assert response.status_code == 200

    response = await client.get(f"/manufacturers/{manufacturers_entry['id']}")
    assert response.status_code == 404
