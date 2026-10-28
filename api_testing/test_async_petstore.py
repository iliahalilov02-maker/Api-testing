# test_async_petstore.py
import pytest
import pytest_asyncio
import time
from async_client import AsyncPetstoreClient

BASE_URL = "https://petstore.swagger.io/v2"

@pytest_asyncio.fixture
async def api_client():
    client = AsyncPetstoreClient(BASE_URL)
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_user_async_crud(api_client):
    username = f"async_user_{int(time.time())}"
    user_data = {
        "id": 0,
        "username": username,
        "firstName": "Async",
        "lastName": "User",
        "email": "async@example.com",
        "password": "pass123",
        "phone": "1234567890",
        "userStatus": 1
    }

    # 1. CREATE
    resp = await api_client.post("user", json=user_data)
    assert resp.status_code == 200

    # 2. GET
    resp = await api_client.get(f"user/{username}")
    assert resp.status_code == 200
    assert resp.json()["username"] == username

    # 3. UPDATE
    user_data["firstName"] = "UpdatedAsync"
    resp = await api_client.put(f"user/{username}", json=user_data)
    assert resp.status_code == 200

    # 4. DELETE
    resp = await api_client.delete(f"user/{username}")
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_store_async_flow(api_client):
    order_id = int(time.time()) % 100000
    order_data = {
        "id": order_id,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2026-10-28T00:00:00.000Z",
        "status": "placed",
        "complete": True
    }

    # 1. PLACE ORDER
    resp = await api_client.post("store/order", json=order_data)
    assert resp.status_code == 200

    # 2. GET ORDER
    resp = await api_client.get(f"store/order/{order_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == order_id

    # 3. INVENTORY
    resp = await api_client.get("store/inventory")
    assert resp.status_code == 200

    # 4. DELETE ORDER
    resp = await api_client.delete(f"store/order/{order_id}")
    assert resp.status_code == 200