from typing import List, Optional
import random

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from ..finances.api.operations import get_operations, create_operation, delete_operation
from ..finances.models.operations import OperationKind, OperationCreate
from ..finances.services.operations import OperationsService

from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter(
    tags=["Pages"]
)


templates = Jinja2Templates(directory="src/templates")


@router.get("/")
def get_operations_list(
        request: Request,
        service: OperationsService = Depends(),
        kind: Optional[OperationKind] = None,
):
    operations = get_operations(kind=kind, service=service)
    image_id = random.randint(1, 5)
    return templates.TemplateResponse("index.html",
                                      {
                                        "request": request,
                                        "operations": operations,
                                        "image_id": image_id})


@router.get("/{kind}")
def get_operations_list_by_kind(
        request: Request,
        kind: str,
        service: OperationsService = Depends(),
):
    operations = get_operations(kind=kind, service=service)
    image_id = random.randint(1, 5)
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "operations":operations,
                                       "image_id": image_id})


@router.post("/add")
def add(
        date: str = Form(...),
        kind: str = Form(...),
        amount: str = Form(...),
        description: str = Form(),
        service: OperationsService = Depends(),
):
    new_operation = OperationCreate(
        date=date,
        kind=kind,
        amount=amount,
        description=description
    )

    create_operation(operation_data=new_operation, service=service)
    url = router.url_path_for('get_operations_list')
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/delete/{operation_id}")
def delete(
        operation_id: int,
        service: OperationsService = Depends(),
):
    delete_operation(operation_id=operation_id, service=service)
    url = router.url_path_for('get_operations_list')
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)