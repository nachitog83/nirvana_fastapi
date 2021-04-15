from fastapi.testclient import TestClient
import mock
import json
from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Challenge"}

class TestMostCommon():
    def _side_effect(self, input, member_id):
        if "https://api1.com" in input:
            return {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}
        elif "https://api2.com" in input:
            return {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}
        elif "https://api3.com" in input:
            return {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}


    def test_calculate_true_values(self):

        with mock.patch("app.routers.get_api_results") as m:
            m.side_effect = self._side_effect
            response = client.get("/insurance/?id=1")
        print(response.text)
        assert response.json()['true_deductible'] == 1000
        assert response.json()['true_stop_loss'] == 10000
        assert response.json()['true_oop_max'] == 6000

class TestAverage():
    def _side_effect(self, input, member_id):
        if "https://api1.com" in input:
            return {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}
        elif "https://api2.com" in input:
            return {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}
        elif "https://api3.com" in input:
            return {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}


    def test_calculate_true_values(self):

        with mock.patch("app.routers.get_api_results") as m:
            m.side_effect = self._side_effect
            response = client.get("/insurance/?id=1&method=average_values")
        assert response.json()['true_deductible'] == 1066.67
        assert response.json()['true_stop_loss'] == 11000
        assert response.json()['true_oop_max'] == 5666.67

class TestValidationError():
    def _side_effect(self, input, member_id):
        if "https://api1.com" in input:
            return {"deductible": 1000, "stop_loss": 10000, "oop_max": 500}
        elif "https://api2.com" in input:
            return {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}
        elif "https://api3.com" in input:
            return {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}


    def test_calculate_true_values(self):

        with mock.patch("app.routers.get_api_results") as m:
            m.side_effect = self._side_effect
            response = client.get("/insurance/?id=2")

        assert response.status_code == 400
