from fastapi import APIRouter, Depends

from src.applications.command.calculate_vlp import calculate_vlp
from src.infrastructures.vlp_repository import VlpRepositoryProtocol
from src.infrastructures.well_repository import WellRepositoryProtocol
from src.models.models import VlpCalcRequest, VlpCalcResponse
from src.routes.stub import Stub

main_router = APIRouter(prefix="/vlp", tags=["VLP"])


@main_router.post("/calc", response_model=VlpCalcResponse)
def calc_vlp(vlp_in: VlpCalcRequest,
             vlp_repo=Depends(Stub(VlpRepositoryProtocol)),
             well_repo=Depends(Stub(WellRepositoryProtocol))
             ):
    """Расчёт VLP по исходным данным и сохранение в Базу"""
    result = calculate_vlp(vlp_repository=vlp_repo,
                           well_repository=well_repo,
                           inclinometry=vlp_in.inclinometry.dict(),
                           casing=vlp_in.casing.dict(),
                           geo_grad=vlp_in.geo_grad,
                           tubing=vlp_in.tubing.dict(),
                           h_res=vlp_in.h_res,
                           pvt=vlp_in.pvt.dict(),
                           p_wh=vlp_in.p_wh,
                           )
    return VlpCalcResponse(**result)
