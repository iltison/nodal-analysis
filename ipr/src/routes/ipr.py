from fastapi import APIRouter

from src.calculations.vogel_ipr import calc_ipr
from src.models.models import IprCalcRequest, IprCalcResponse

main_router = APIRouter(prefix="/ipr", tags=["IPR"])


@main_router.post("/calc", response_model=IprCalcResponse)
async def calc_ipr_router(ipr_in: IprCalcRequest):
    return calc_ipr(p_res=ipr_in.p_res,
                    pi=ipr_in.pi,
                    wct=ipr_in.wct,
                    pb=ipr_in.pb,
                    points=ipr_in.points
                    )
