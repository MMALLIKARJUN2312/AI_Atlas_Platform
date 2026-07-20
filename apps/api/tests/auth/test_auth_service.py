import pytest
from fastapi import HTTPException

from app.auth.schemas import LoginRequest
from app.auth.service import AuthService
from app.core.security import hash_password


class FakeUser:
    def __init__(self, email, hashed_password, is_active=True, role="admin"):
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.role = role


class FakeDb:
    def __init__(self, user=None):
        self._user = user

    async def scalar(self, statement):
        return self._user


@pytest.mark.asyncio
async def test_login_succeeds_with_correct_password():
    user = FakeUser(email="admin@aiatlas.local", hashed_password=hash_password("secret123"))
    service = AuthService(FakeDb(user=user))

    token = await service.login(LoginRequest(email="admin@aiatlas.local", password="secret123"))

    assert token.token_type == "bearer"
    assert token.access_token


@pytest.mark.asyncio
async def test_login_rejects_wrong_password():
    user = FakeUser(email="admin@aiatlas.local", hashed_password=hash_password("secret123"))
    service = AuthService(FakeDb(user=user))

    with pytest.raises(HTTPException) as error:
        await service.login(LoginRequest(email="admin@aiatlas.local", password="wrong"))
    assert error.value.status_code == 401


@pytest.mark.asyncio
async def test_login_rejects_unknown_email():
    service = AuthService(FakeDb(user=None))

    with pytest.raises(HTTPException) as error:
        await service.login(LoginRequest(email="nobody@example.com", password="whatever"))
    assert error.value.status_code == 401


@pytest.mark.asyncio
async def test_login_rejects_inactive_user():
    user = FakeUser(email="admin@aiatlas.local", hashed_password=hash_password("secret123"), is_active=False)
    service = AuthService(FakeDb(user=user))

    with pytest.raises(HTTPException) as error:
        await service.login(LoginRequest(email="admin@aiatlas.local", password="secret123"))
    assert error.value.status_code == 401
