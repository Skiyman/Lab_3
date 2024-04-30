from models.manufacturer import ManufacturerModel
from test.test_route_manufacturer import manufacturers_entry
from test.test_fixtures import *


@pytest.fixture
async def car_entry(client: AsyncClient, manufacturers_entry: ManufacturerModel):
    response = await client.post("/cars", json={
        "manufacturer_id": manufacturers_entry["id"],
        "name": "2114",
        "production_year": "2012-04-30"
    })
    body = response.json()

    assert response.status_code == 200
    assert body["manufacturer_id"] == manufacturers_entry["id"]
    assert body["name"] == "2114"
    assert body["production_year"] == "2012-04-30"

    return body, manufacturers_entry


async def test_list_car(client: AsyncClient, car_entry):
    car, manufacturer = car_entry
    response = await client.get("/cars")
    body = response.json()

    assert response.status_code == 200
    assert body[0]["id"] == car["id"]
    assert body[0]["name"] == car["name"]
    assert body[0]["production_year"] == car["production_year"]
    assert body[0]["manufacturer_id"] == manufacturer["id"]


async def test_get_car(client: AsyncClient, car_entry):
    car, manufacturer = car_entry
    response = await client.get(f"/cars/{car['id']}")
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == car["id"]
    assert body["name"] == car["name"]
    assert body["production_year"] == car["production_year"]
    assert body["manufacturer_id"] == manufacturer["id"]


async def test_patch_car(client: AsyncClient, car_entry):
    car, manufacturer = car_entry
    response = await client.patch(f"/cars/{car['id']}", json={
        "name": "Granta"
    })
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == car["id"]
    assert body["name"] == "Granta"
    assert body["production_year"] == car["production_year"]
    assert body["manufacturer_id"] == manufacturer["id"]


async def test_override_car(client: AsyncClient, car_entry):
    car, manufacturer = car_entry
    response = await client.put(f"/cars/{car['id']}", json={
        "manufacturer_id": manufacturer["id"],
        "name": "Granta",
        "production_year": "2018-04-30"
    })
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == car["id"]
    assert body["name"] == "Granta"
    assert body["production_year"] == "2018-04-30"
    assert body["manufacturer_id"] == manufacturer["id"]


async def test_delete_car(client: AsyncClient, car_entry):
    car, _ = car_entry
    response = await client.get(f"/cars/{car['id']}")
    assert response.status_code == 200

    response = await client.delete(f"/cars/{car['id']}")
    assert response.status_code == 200

    response = await client.get(f"/cars/{car['id']}")
    assert response.status_code == 404
