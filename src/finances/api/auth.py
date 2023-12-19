from fastapi import APIRouter, Depends
from ..models.auth import (
    User,
    UserCreate,
    Token,
)
from ..services.auth import AuthService, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)


@router.post("/sign-up", response_model=Token)
def sign_up(
        user_data: UserCreate,
        service: AuthService = Depends()
):
    return service.register_new_user(user_data)


@router.post("/sign-in", response_model=Token)
def sign_in(
        username: str,
        password: str,
        service: AuthService = Depends()
):
    return service.authenticate_user(
        username,
        password,
    )


@router.get("/user", response_model=User)
def get_user(
        token: str):
    return get_current_user(token)



