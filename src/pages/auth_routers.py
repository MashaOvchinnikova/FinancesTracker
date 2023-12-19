from fastapi import APIRouter, Request, Depends, Form

from fastapi.templating import Jinja2Templates

from ..finances.api.auth import sign_up, sign_in, get_user
from ..finances.models.auth import UserCreate
from ..finances.services.auth import AuthService

from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter(
    tags=["Pages"],
    prefix='/auth'
)


templates = Jinja2Templates(directory="src/templates")


@router.get("/sign-up")
def get_signup_page(
        request: Request
):
    return templates.TemplateResponse("signup.html",
                                      {"request": request})


@router.get("/sign-in")
def get_login_page(
        request: Request
):
    return templates.TemplateResponse("login.html",
                                      {"request": request})


@router.post("/sign-up")
def sign_up_user(
        email: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        service: AuthService = Depends()
):
    user_data = UserCreate(email=email,username=username,password=password)
    sign_up(user_data=user_data, service=service)
    url = router.url_path_for('get_login_page')
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.post("/sign-in")
def sign_in_user(
        username: str = Form(...),
        password: str = Form(...),
        service: AuthService = Depends()
):
    access_token = sign_in(
        username=username,
        password=password,
        service=service).access_token
    url = router.url_path_for('get_user_page',token=access_token)
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/user/{token}")
def get_user_page(
        request:Request,
        token: str):
    user = get_user(token)
    return templates.TemplateResponse("user.html",
                                      {"request": request,
                                       "user": user})
