import asyncio, pytest
from typing import AsyncGenerator
from uuid import UUID
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Header
from src.keystone.main import app
from src.keystone.core.db import Base
from src.keystone.models.tenant import Tenant
from src.keystone.models.role import Role
from src.keystone.models.user import User
from src.keystone.api.invitations import get_db, get_current_user
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    async def setup():
        async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    asyncio.run(setup())
    yield
    async def teardown():
        async with engine.begin() as conn: await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(teardown())
@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    connection = await engine.connect()
    transaction = await connection.begin()
    async_session = TestingSessionLocal(bind=connection)
    try: yield async_session
    finally:
        await async_session.close()
        await transaction.rollback()
        await connection.close()
@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]: yield db_session
    async def override_get_current_user(x_test_user_id: str | None = Header(None, alias="X-Test-User-Id")) -> User | None:
        if not x_test_user_id: return None
        return await db_session.get(User, UUID(x_test_user_id))
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    async with AsyncClient(app=app, base_url="http://test") as c: yield c
    app.dependency_overrides.clear()
@pytest.fixture(scope="function")
async def default_tenant(db_session: AsyncSession) -> Tenant:
    tenant = Tenant(name="Default Test Tenant")
    db_session.add(tenant)
    await db_session.commit()
    return tenant
@pytest.fixture(scope="function")
async def admin_role(db_session: AsyncSession, default_tenant: Tenant) -> Role:
    role = Role(name="Administrateur", tenant_id=default_tenant.id)
    db_session.add(role)
    await db_session.commit()
    return role
@pytest.fixture(scope="function")
async def employee_role(db_session: AsyncSession) -> Role:
    role = Role(name="Employé", tenant_id=None)
    db_session.add(role)
    await db_session.commit()
    return role
@pytest.fixture(scope="function")
async def admin_user(db_session: AsyncSession, default_tenant: Tenant, admin_role: Role) -> User:
    user = User(email="admin@test.com", hashed_password="fake_password", tenant_id=default_tenant.id)
    user.roles.append(admin_role)
    db_session.add(user)
    await db_session.commit()
    return user
@pytest.fixture
def admin_user_headers(admin_user: User) -> dict[str, str]: return {"X-Test-User-Id": str(admin_user.id)}
@pytest.fixture
def default_role_id(employee_role: Role) -> UUID: return employee_role.id
