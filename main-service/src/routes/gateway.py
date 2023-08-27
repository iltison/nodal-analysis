import asyncio

from fastapi import APIRouter, HTTPException, status

from back.config import get_gateway_timeout
from back.models.models import (WellModelCalcRequest, WellModelCalcResponse, HTTPError)
from back.routes.request_formers import (form_ipr_request,
                                         form_nodal_request,
                                         form_vlp_request)

main_router = APIRouter(prefix="/well_model", tags=["WellModel"])


@main_router.put("/calc",
                 responses={status.HTTP_200_OK: {"model": WellModelCalcResponse},
                            status.HTTP_409_CONFLICT: {"model": HTTPError,
                                                       "description": "Пользовательская ошибка", },
                            status.HTTP_504_GATEWAY_TIMEOUT: {"model": HTTPError,
                                                              "description": "Ошибка на стороне сервера", },
                            })
async def my_profile(data: WellModelCalcRequest):
    res_vlp = asyncio.create_task(form_vlp_request(data))
    res_ipr = asyncio.create_task(form_ipr_request(data))

    tasks = [res_vlp, res_ipr]
    done, pending = await asyncio.wait(tasks, timeout=get_gateway_timeout())

    if res_vlp in pending or res_ipr in pending:
        [task.cancel() for task in tasks]
        raise HTTPException(status_code=504, detail="service timeout")
    if res_vlp.exception() is not None or res_ipr.exception() is not None:
        [task.cancel() for task in tasks]
        raise HTTPException(status_code=409, detail="Ошибка в переданных данных")

    res_vlp = res_vlp.result()
    res_ipr = res_ipr.result()
    nodal = await form_nodal_request(res_vlp, res_ipr)
    return WellModelCalcResponse(vlp=res_vlp, ipr=res_ipr, nodal=nodal)
