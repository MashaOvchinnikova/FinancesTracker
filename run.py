import uvicorn
from src.finances.setting import settings
from src.finances.main import app


if __name__ == '__main__':
    uvicorn.run(app=app,
                host=settings.server_host,
                port=settings.server_port,
                )
