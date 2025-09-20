from uuid import UUID

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_create_invitation_as_admin(
    client: AsyncClient, admin_user_headers: dict, default_role_id: UUID
):
    email_to_invite = "nouvel.employe@example.com"
    invitation_data = {"email": email_to_invite, "role_id": str(default_role_id)}
    response = await client.post(
        "/api/v1/invitations/", json=invitation_data, headers=admin_user_headers
    )
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}: {response.text}"

    data = response.json()
    assert data["email"] == email_to_invite
    assert data["status"] == "pending"
    assert "id" in data
    assert data["role_id"] == str(default_role_id)
