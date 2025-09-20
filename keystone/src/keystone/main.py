from fastapi import FastAPI
from src.keystone.api import invitations
app = FastAPI(title="Keystone API")
app.include_router(invitations.router, prefix="/api/v1/invitations", tags=["invitations"])
@app.get("/healthcheck")
async def healthcheck(): return {"status": "ok"}
