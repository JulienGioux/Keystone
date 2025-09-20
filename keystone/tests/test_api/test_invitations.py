import pytest
from httpx import AsyncClient
from uuid import UUID

pytestmark = pytest.mark.anyio

async def test_create_invitation_as_admin(
    client: AsyncClient,
    admin_user_headers: dict,
    default_role_id: UUID
):
    """
    Vérifie qu'un administrateur authentifié peut créer une invitation avec succès.
    """
    email_to_invite = "nouvel.employe@example.com"
    invitation_data = {
        "email": email_to_invite,
        "role_id": str(default_role_id)
    }

    response = await client.post(
        "/api/v1/invitations/",
        json=invitation_data,
        headers=admin_user_headers
    )
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
