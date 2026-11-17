from fastapi import APIRouter, status

from src.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from src.platform.errors import NotImplementedYet

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    # TODO: service.register(body) -> hash password, create user, return JWT
    raise NotImplementedYet("auth.register")


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    # TODO: service.login(body) -> verify password, return JWT
    raise NotImplementedYet("auth.login")