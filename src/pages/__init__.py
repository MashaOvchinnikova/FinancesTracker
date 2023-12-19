from fastapi import APIRouter

from .operations_routers import router as operations_router
from .auth_routers import router as auth_router
from .chat_routers import router as chat_router

router = APIRouter()
router.include_router(operations_router)
router.include_router(auth_router)
router.include_router(chat_router)
