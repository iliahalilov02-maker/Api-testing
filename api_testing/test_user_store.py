import pprint
import time
import requests

from api_testing.base_request import BaseRequest, BASE_URL_PETSTORE


class ExtendedRequest(BaseRequest):
    """Расширяем базовый класс: добавляем PUT и POST с json-телом."""

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = requests.put(url, json=body)
        self._log('PUT', response)
        return response

    def post_json(self, endpoint, body, expected_error=False):
        """POST без endpoint_id (например, /user, /store/order)."""
        url = f'{self.base_url}/{endpoint}'
        response = requests.post(url, json=body)
        self._log('POST', response)
        return response

    def get_plain(self, endpoint, expected_error=False):
        """GET без endpoint_id (например, /store/inventory)."""
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url)
        self._log('GET', response)
        return response

    @staticmethod
    def _log(method, response):
        pprint.pprint(f'{method} example')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        pprint.pprint(response.text)
        pprint.pprint('**********')


base = ExtendedRequest(BASE_URL_PETSTORE)


#  USER: 4 запроса 

def test_user_create_get_update_delete():
    username = f"test_user_{int(time.time())}"
    user_body = {
        "id": 0,
        "username": username,
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "pass123",
        "phone": "1234567890",
        "userStatus": 1,
    }

    # 1. CREATE — POST /user
    resp = base.post_json("user", user_body)
    assert resp.status_code == 200

    # 2. GET — GET /user/{username}
    resp = base.get("user", username)
    assert resp["username"] == username

    # 3. UPDATE — PUT /user/{username}
    user_body["firstName"] = "Updated"
    resp = base.put("user", username, user_body)
    assert resp.status_code == 200

    # 4. DELETE — DELETE /user/{username}
    msg = base.delete("user", username)
    pprint.pprint(f"delete user: {msg}")


#  STORE: 4 запроса 

def test_store_place_get_inventory_delete():
    order_id = int(time.time()) % 100000
    order_body = {
        "id": order_id,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2026-10-28T00:00:00.000Z",
        "status": "placed",
        "complete": True,
    }

    # 1. PLACE ORDER — POST /store/order
    resp = base.post_json("store/order", order_body)
    assert resp.status_code == 200

    # 2. GET ORDER — GET /store/order/{orderId}
    resp = base.get("store/order", order_id, expected_error=True)
    pprint.pprint(resp)

    # 3. INVENTORY — GET /store/inventory
    resp = base.get_plain("store/inventory")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)

    # 4. DELETE ORDER — DELETE /store/order/{orderId}
    msg = base.delete("store/order", order_id)
    pprint.pprint(f"delete order: {msg}")