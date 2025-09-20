from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.crud import invitations as invitations_crud
from src.keystone.crud import users as users_crud
from src.keystone.api.invitations import get_db
from src.keystone.schemas.user import User, UserCreate

router = APIRouter()


@router.post(
    "/register-with-invitation/{token}",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def register_with_invitation(
    *,
    db: AsyncSession = Depends(get_db),
    token: str,
    user_in: UserCreate,
):
    invitation = await invitations_crud.get_by_token(db, token=token)
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found or has expired.",
        )

    if invitation.email != user_in.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation email does not match provided email.",
        )

    user = await users_crud.create_user_from_invitation(
        db, invitation=invitation, user_in=user_in
    )
    return user
