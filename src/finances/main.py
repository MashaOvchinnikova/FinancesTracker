from fastapi import FastAPI, Request
from .api import router as api_router
from ..pages import router as pages_router
from fastapi.staticfiles import StaticFiles
from ..chat.router import router as chat_router

app = FastAPI(
    title="FinancesTracker"
)

app.include_router(api_router)
app.include_router(pages_router)
app.include_router(chat_router)


app.mount("/static", StaticFiles(directory="src/static"), name="static")





