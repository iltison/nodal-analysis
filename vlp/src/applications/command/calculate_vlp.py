from dataclasses import asdict

import numpy as np

from src.calculations.well import calc_pwf
from src.domain.vlp import Vlp, Inclinometry, Pipeline, Tubing, PVT
from src.domain.well import Well
from src.infrastructures.vlp_repository import VlpRepositoryProtocol
from src.infrastructures.well_repository import WellRepositoryProtocol


def calculate_vlp(vlp_repository: VlpRepositoryProtocol,
                  well_repository: WellRepositoryProtocol,
                  inclinometry: dict,
                  casing: dict,
                  tubing: dict,
                  pvt: dict,
                  p_wh: float,
                  geo_grad: float,
                  h_res: float) -> dict:
    vlp = Vlp(inclinometry=Inclinometry(MD=inclinometry['MD'], TVD=inclinometry['TVD']),
              casing=Pipeline(diameter=casing['d']),
              tubing=Tubing(diameter=tubing['d'], h_mes=tubing['h_mes']),
              pvt=PVT(wct=pvt['wct'], rp=pvt['rp'], gamma_oil=pvt['gamma_oil'], gamma_gas=pvt['gamma_gas'],
                      gamma_wat=pvt['gamma_wat'], t_res=pvt['t_res'], ),
              p_wh=p_wh,
              geo_grad=geo_grad,
              h_res=h_res,
              )
    vlp.set_hash_id()

    # Если входные данные рассчитывались то возвращаем
    if well_result := well_repository.get(vlp.id):
        return {"q_liq": well_result.q_liq, "p_wf": well_result.p_wf}
    else:
        vlp_repository.add(vlp)

        # Расчет сторонним пакетом
        q_liq = np.linspace(0.001, 400, 7)
        p_wf = np.empty_like(q_liq)
        for i, ql in enumerate(q_liq):
            p_wf[i] = calc_pwf(inclinometry, casing, tubing, pvt, p_wh, geo_grad, h_res, ql)

        well = Well(id=vlp.id,
                    q_liq=q_liq.tolist(),
                    p_wf=p_wf.tolist(),
                    )
        well_repository.add(well)
        return asdict(well)
