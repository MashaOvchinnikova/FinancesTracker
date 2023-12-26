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
def get_chat_page(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    # return templates.TemplateResponse("chat.html", {"request": request})
    return templates.TemplateResponse("chat.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})
