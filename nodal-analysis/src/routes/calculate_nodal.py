from fastapi import APIRouter

from src.calculations.nodal import calc_nodal
from src.models.models import NodalCalcRequest, NodalCalcResponse

main_router = APIRouter(prefix="/nodal", tags=["NodalAnalysis"])


@main_router.post("/calc", response_model=NodalCalcResponse)
async def calculate_nodal_controller(data: NodalCalcRequest):
    """
    Эндпоинт для выполнения Узлового Анализа
    """
    res = calc_nodal(vlp=data.vlp.dict(), ipr=data.ipr.dict())
    return NodalCalcResponse(__root__=res)
