import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.models.user import User
from src.keystone.models.invitation import Invitation
from src.keystone.crud.invitations import get_by_token

pytestmark = pytest.mark.anyio


async def test_register_with_valid_invitation(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user_headers: dict,
    employee_role,
):
    # 1. Create an invitation via the API
    email_to_invite = "new.user@example.com"
    invitation_data = {"email": email_to_invite, "role_id": str(employee_role.id)}
    response = await client.post(
        "/api/v1/invitations/", json=invitation_data, headers=admin_user_headers
    )
    assert response.status_code == 201
    invitation_token = response.json()["token"]

    # 2. Register user with the invitation token
    registration_data = {
        "email": email_to_invite,
        "password": "a_strong_password",
    }
    response = await client.post(
        f"/api/v1/users/register-with-invitation/{invitation_token}",
        json=registration_data,
    )

    # 3. Assert response
    assert response.status_code == 201, response.text
    user_data = response.json()
    assert user_data["email"] == email_to_invite

    # 4. Assert user creation in DB
    user = await db_session.get(User, uuid.UUID(user_data["id"]))
    assert user is not None
    assert user.email == email_to_invite

    # 5. Assert tenant association
    assert str(user.tenant_id) == user_data["tenant_id"]

    # 6. Assert role association
    await db_session.refresh(user, ["roles"])
    assert len(user.roles) == 1
    assert user.roles[0].id == employee_role.id

    # 7. Assert invitation status
    invitation = await get_by_token(db_session, token=invitation_token)
    assert invitation is None

    # Also check the invitation status by getting it directly from the db
    # This is to make sure the get_by_token function is working correctly
    # by not returning an accepted invitation
    statement = select(Invitation).where(Invitation.token == invitation_token)
    result = await db_session.execute(statement)
    invitation_from_db = result.scalar_one()
    assert invitation_from_db.status == "accepted"
