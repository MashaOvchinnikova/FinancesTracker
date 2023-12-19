from fastapi import APIRouter, Request, Depends, Form

from fastapi.templating import Jinja2Templates

from ..finances.api.auth import sign_up, sign_in, get_user
from ..finances.models.auth import UserCreate
from ..finances.services.auth import AuthService

from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter(
    tags=["Pages"],
    prefix='/chat'
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/chat")
def get_chat_page(request:Request):
    return templates.TemplateResponse("chat.html", {"request": request})

