import aiohttp

from back.config import get_vlp_host, get_ipr_host, get_nodal_host
from back.models.models import (IprCalcRequest, NodalCalcRequest,
                                VlpCalcRequest, WellModelCalcRequest, VlpIprCalcResponse, NodalCalcResponse)


async def form_vlp_request(well_model_request):
    data = VlpCalcRequest(**well_model_request.dict())
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{get_vlp_host()}/calc", json=data.dict()) as response:
            result = await response.json()
            return VlpIprCalcResponse(**result)


async def form_ipr_request(well_model_request: WellModelCalcRequest):
    data = IprCalcRequest(p_res=well_model_request.p_res,
                          wct=well_model_request.pvt.wct,
                          pi=well_model_request.pi,
                          pb=well_model_request.pvt.pb,
                          )
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{get_ipr_host()}/calc", json=data.dict()) as response:
            result = await response.json()
            return VlpIprCalcResponse(**result)


async def form_nodal_request(vlp_result, ipr_result):
    data = NodalCalcRequest(vlp=vlp_result,
                            ipr=ipr_result,
                            )
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{get_nodal_host()}/calc", json=data.dict()) as response:
            result = await response.json()
            return NodalCalcResponse(__root__=result)
