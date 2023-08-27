import uvicorn
from fastapi import FastAPI

from src.infrastructures.db import get_session
from src.infrastructures.vlp_repository import VlpRepositoryDatabase, VlpRepositoryProtocol
from src.infrastructures.well_repository import WellRepositoryDatabase, WellRepositoryProtocol
from src.routes.vlp import main_router

app = FastAPI()

app.include_router(main_router)

app.dependency_overrides[VlpRepositoryProtocol] = lambda: VlpRepositoryDatabase(get_session())
app.dependency_overrides[WellRepositoryProtocol] = lambda: WellRepositoryDatabase(get_session())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
