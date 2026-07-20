import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.api.deps import get_current_admin_user
from app.core.security import create_access_token


class FakeUser:
    def __init__(self, email="admin@aiatlas.local", role="admin", is_active=True):
        self.email = email
        self.role = role
        self.is_active = is_active


class FakeDb:
    def __init__(self, user=None):
        self._user = user

    async def scalar(self, statement):
        return self._user


def _bearer(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


@pytest.mark.asyncio
async def test_rejects_missing_credentials():
    with pytest.raises(HTTPException) as error:
        await get_current_admin_user(db=FakeDb(), credentials=None)
    assert error.value.status_code == 401


@pytest.mark.asyncio
async def test_rejects_invalid_token():
    with pytest.raises(HTTPException) as error:
        await get_current_admin_user(db=FakeDb(), credentials=_bearer("not-a-real-token"))
    assert error.value.status_code == 401


@pytest.mark.asyncio
async def test_rejects_token_for_unknown_user():
    token = create_access_token(subject="ghost@example.com", role="admin")
    with pytest.raises(HTTPException) as error:
        await get_current_admin_user(db=FakeDb(user=None), credentials=_bearer(token))
    assert error.value.status_code == 403


@pytest.mark.asyncio
async def test_rejects_non_admin_role():
    token = create_access_token(subject="user@example.com", role="user")
    user = FakeUser(email="user@example.com", role="user")
    with pytest.raises(HTTPException) as error:
        await get_current_admin_user(db=FakeDb(user=user), credentials=_bearer(token))
    assert error.value.status_code == 403


@pytest.mark.asyncio
async def test_rejects_inactive_admin():
    token = create_access_token(subject="admin@aiatlas.local", role="admin")
    user = FakeUser(is_active=False)
    with pytest.raises(HTTPException) as error:
        await get_current_admin_user(db=FakeDb(user=user), credentials=_bearer(token))
    assert error.value.status_code == 403


@pytest.mark.asyncio
async def test_accepts_valid_admin_token():
    token = create_access_token(subject="admin@aiatlas.local", role="admin")
    user = FakeUser()

    result = await get_current_admin_user(db=FakeDb(user=user), credentials=_bearer(token))

    assert result is user
