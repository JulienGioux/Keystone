from fastapi import APIRouter
from src.keystone.models.user import User
async def get_current_user() -> User | None: return None
router = APIRouter()
@router.get("/")
async def get_invitations(): return []
