from fastapi import FastAPI

from src.keystone.api import invitations, users

app = FastAPI(title="Keystone API")
app.include_router(
    invitations.router, prefix="/api/v1/invitations", tags=["invitations"]
)
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
