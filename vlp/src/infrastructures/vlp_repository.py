from abc import ABC, abstractmethod  # Protocol don't work with dependency_overrides

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.vlp import Vlp, Pipeline, Tubing, PVT, Inclinometry
from src.tables.models import VLPModel


class VlpRepositoryProtocol(ABC):
    @abstractmethod
    def get(self, id: str) -> Vlp | None:
        """
        Получение данных
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def add(self, entity: Vlp):
        """
        Добавление данных
        :return:
        """
        raise NotImplemented


class WellDataMapper:
    def entity_to_model(self, entity: Vlp) -> VLPModel:
        return VLPModel(
            id=entity.id,
            md=entity.inclinometry.MD,
            tvd=entity.inclinometry.TVD,
            casing_d=entity.casing.diameter,
            tubing_d=entity.tubing.diameter,
            tubing_h_mes=entity.tubing.h_mes,
            pvt_wct=entity.pvt.wct,
            pvt_rp=entity.pvt.rp,
            pvt_gamma_oil=entity.pvt.gamma_oil,
            pvt_gamma_gas=entity.pvt.gamma_gas,
            pvt_gamma_wat=entity.pvt.gamma_wat,
            pvt_t_res=entity.pvt.t_res,
            p_wh=entity.p_wh,
            geo_grad=entity.geo_grad,
            h_res=entity.h_res,
        )

    def model_to_entity(self, model: VLPModel) -> Vlp:
        return Vlp(inclinometry=Inclinometry(MD=model.md, TVD=model.tvd),
                   casing=Pipeline(diameter=model.casing_d),
                   tubing=Tubing(diameter=model.tubing_d, h_mes=model.tubing_h_mes),
                   pvt=PVT(wct=model.pvt_wct, rp=model.pvt_rp, gamma_oil=model.pvt_gamma_oil,
                           gamma_gas=model.pvt_gamma_gas,
                           gamma_wat=model.pvt_gamma_wat, t_res=model.pvt_t_res),
                   p_wh=model.p_wh,
                   geo_grad=model.geo_grad,
                   h_res=model.h_res,
                   )


class VlpRepositoryDatabase(VlpRepositoryProtocol, WellDataMapper):
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: str) -> Vlp | None:
        """
        Получение данных
        :return:
        """
        result = self.session.scalars(select(Vlp).where(Vlp.id == id)).one_or_none()
        if result:
            return self.model_to_entity(result)
        return None

    def add(self, entity: Vlp):
        """
        Добавление данных
        :return:
        """

        self.session.add(self.entity_to_model(entity))
        self.session.commit()
