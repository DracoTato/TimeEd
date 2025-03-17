from datetime import date

from app.db.schema.models import User
from app.db.schema.enums import Gender, User_Type
from app.db import db


class TestGlobal:
    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"TimeED" in response.data

    def test_not_found(self, client):
        response = client.get("/not-found/")
        assert response.status_code == 404


class TestRegister:
    def register(self, client, **kwargs):
        defualt_data = {
            "full_name": "test test",
            "birthdate": date(2000, 1, 1),
            "email": "test@gmail.com",
            "password": "test123@#$",
            "confirm_password": "test123@#$",
            "gender": Gender.MALE.value,
            "account_type": User_Type.STUDENT.value,
        }
        defualt_data.update(kwargs)

        return client.post("/auth/register/", data=defualt_data)

    def test_get(self, client):
        response = client.get("/auth/register/")
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_post_success(self, client):
        response = self.register(client)

        assert response.status_code == 302

    def test_post_bad_email(self, client):
        response = self.register(client, email="bad-email")

        assert response.status_code == 200

    def test_post_bad_password(self, client):
        response = self.register(client, password="0" * 6, confirm_password="0" * 6)

        assert 1
        assert response.status_code == 200

    def test_post_bad_confirm(self, client):
        response = self.register(client, confirm_password="dont-match")

        assert b"Passwords don" in response.data
        assert response.status_code == 200

    def test_post_bad_account_type(self, client):
        response = self.register(client, account_type=100)

        assert b"Please choose one." in response.data
        assert response.status_code == 200

    def test_post_bad_gender(self, client):
        response = self.register(client, gender=20)

        assert b"Please choose one." in response.data
        assert response.status_code == 200


class TestLogin:
    def test_get(self, client):
        response = client.get("/auth/login/")
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_post_success(self, app, client):
        test_user = User(
            full_name="test test",
            birthdate=date(2000, 1, 1),
            email="test@gmail.com",
            password="test123456",
            gender=Gender.MALE,
            role=User_Type.STUDENT,
        )

        with app.app_context():
            db.session.add(test_user)
            db.session.commit()

        response = client.post(
            "/auth/login/",
            data=dict(
                email="test@gmail.com",
                password="test123456",
            ),
        )

        assert response.status_code == 302
