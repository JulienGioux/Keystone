import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.models.team import Team
from src.keystone.models.tenant import Tenant

pytestmark = pytest.mark.anyio


async def test_create_team_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user_headers: dict,
):
    team_data = {"name": "Équipe de développement"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=admin_user_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == team_data["name"]
    assert "id" in data


async def test_create_team_as_non_admin(
    client: AsyncClient,
    employee_user_headers: dict,
):
    team_data = {"name": "Équipe non autorisée"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=employee_user_headers
    )
    assert response.status_code == 403


async def test_list_teams(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user_headers: dict,
    default_tenant,
):
    # Create a team in the default tenant
    team1_data = {"name": "Équipe du premier tenant"}
    response = await client.post(
        "/api/v1/teams/", json=team1_data, headers=admin_user_headers
    )
    assert response.status_code == 201

    # Create a second tenant and team to ensure we only get teams from the current tenant
    tenant2 = Tenant(name="Second Test Tenant")
    db_session.add(tenant2)
    await db_session.commit()
    team2 = Team(name="Équipe du deuxième tenant", tenant_id=tenant2.id)
    db_session.add(team2)
    await db_session.commit()

    response = await client.get("/api/v1/teams/", headers=admin_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == team1_data["name"]
    assert data[0]["tenant_id"] == str(default_tenant.id)


async def test_add_member_to_team(
    client: AsyncClient,
    admin_user_headers: dict,
    employee_user,
):
    # Create a team
    team_data = {"name": "Équipe de test"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=admin_user_headers
    )
    assert response.status_code == 201
    team_id = response.json()["id"]

    # Add employee to the team
    add_member_data = {"user_id": str(employee_user.id), "role": "member"}
    response = await client.post(
        f"/api/v1/teams/{team_id}/members",
        json=add_member_data,
        headers=admin_user_headers,
    )
    assert response.status_code == 201


async def test_add_member_with_invalid_role(
    client: AsyncClient,
    admin_user_headers: dict,
    employee_user,
):
    # Create a team
    team_data = {"name": "Équipe de test"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=admin_user_headers
    )
    team_id = response.json()["id"]

    # Add employee with invalid role
    add_member_data = {"user_id": str(employee_user.id), "role": "invalid_role"}
    response = await client.post(
        f"/api/v1/teams/{team_id}/members",
        json=add_member_data,
        headers=admin_user_headers,
    )
    assert response.status_code == 422


async def test_add_non_existent_user_to_team(
    client: AsyncClient,
    admin_user_headers: dict,
):
    # Create a team
    team_data = {"name": "Équipe de test"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=admin_user_headers
    )
    team_id = response.json()["id"]

    import uuid
    non_existent_user_id = str(uuid.uuid4())

    # Add non-existent user
    add_member_data = {"user_id": non_existent_user_id, "role": "member"}
    response = await client.post(
        f"/api/v1/teams/{team_id}/members",
        json=add_member_data,
        headers=admin_user_headers,
    )
    assert response.status_code == 404


async def test_add_member_to_non_existent_team(
    client: AsyncClient,
    admin_user_headers: dict,
    employee_user,
):
    import uuid
    non_existent_team_id = str(uuid.uuid4())

    # Add employee to non-existent team
    add_member_data = {"user_id": str(employee_user.id), "role": "member"}
    response = await client.post(
        f"/api/v1/teams/{non_existent_team_id}/members",
        json=add_member_data,
        headers=admin_user_headers,
    )
    assert response.status_code == 404


async def test_add_member_as_non_admin(
    client: AsyncClient,
    admin_user_headers: dict,
    employee_user_headers: dict,
    employee_user,
):
    # Create a team as admin
    team_data = {"name": "Équipe de test"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=admin_user_headers
    )
    team_id = response.json()["id"]

    # Try to add a member as employee
    add_member_data = {"user_id": str(employee_user.id), "role": "member"}
    response = await client.post(
        f"/api/v1/teams/{team_id}/members",
        json=add_member_data,
        headers=employee_user_headers,
    )
    assert response.status_code == 403


async def test_add_existing_member_to_team(
    client: AsyncClient,
    admin_user_headers: dict,
    employee_user,
):
    # Create a team
    team_data = {"name": "Équipe de test"}
    response = await client.post(
        "/api/v1/teams/", json=team_data, headers=admin_user_headers
    )
    assert response.status_code == 201
    team_id = response.json()["id"]

    # Add employee to the team
    add_member_data = {"user_id": str(employee_user.id), "role": "member"}
    response = await client.post(
        f"/api/v1/teams/{team_id}/members",
        json=add_member_data,
        headers=admin_user_headers,
    )
    assert response.status_code == 201

    # Try to add the same employee again
    response = await client.post(
        f"/api/v1/teams/{team_id}/members",
        json=add_member_data,
        headers=admin_user_headers,
    )
    assert response.status_code == 400
