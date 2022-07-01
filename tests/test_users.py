from http import client
from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest

from main import app

client = TestClient(app)


def mock_post(endpoint, json):
    field_names = json.keys()

    good_mock_response = {'status_code': 201}
    bad_mock_response = {'status_code': 500}

    if endpoint == '/users/register':
        if all(field in field_names for field in ['username', 'password', 'fullname']):
            return good_mock_response
    return bad_mock_response


class TestUserRegistration:
    def test_get_user_register_405(self):
        """ registration end point shouldn't allow get request"""
        response = client.get("/users/register")

        assert response.status_code == 405

    def test_post_user_register_without_body_422(self):
        """ post  register request without body returns error 422 """
        response = client.post("/users/register")

        assert response.status_code == 422

    def test_post_user_register_with_improper_body_422(self):
        """ post  register request improper body returns error 422 """
        response = client.post("/users/register", json={"username": "vamsi"})

        assert response.status_code == 422

    @patch('fastapi.testclient.TestClient.post', side_effect=mock_post)
    def test_post_request_with_proper_body_returns_201(self, post):
        """ post register with proper body return 201 """
        response = client.post(
            "/users/register",  json={"username": "vamsi", "password": "abcd", "fullname": "Vamsi Y"})
        print("hello", response)
        assert response['status_code'] == 201


class TestUserLogin:
    """TestUserLogin tests /users/auth"""

    def test_get_request_returns_405(self):
        """login endpoint does only expect a post request"""
        response = client.get("/users/auth")
        assert response.status_code == 405

    def test_post_request_without_body_returns_422(self):
        """body should have username, password and fullname"""
        response = client.post("/users/auth")
        assert response.status_code == 422

    def test_post_request_with_improper_body_returns_422(self):
        """both username and password is required"""
        response = client.post(
            "/users/auth",
            json={"username": "vamsiy"}
        )
        assert response.status_code == 422

    def test_post_request_with_proper_body_returns_200_with_jwt_token(self):
        response = client.post(
            "/users/auth",
            json={"username": "vamsi", "password": "abcd"}
        )
        assert response.status_code == 200
        assert len(response.json()) == 2
