from abc import ABC, abstractmethod  # Protocol don't work with dependency_overrides

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.well import Well
from src.tables.models import WellData


class WellRepositoryProtocol(ABC):
    @abstractmethod
    def get(self, id: str) -> Well | None:
        """
        Получение данных
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def add(self, entity: Well):
        """
        Добавление данных
        :return:
        """
        raise NotImplemented


class WellRepositoryDatabase(WellRepositoryProtocol):
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: str) -> Well | None:
        """
        Получение данных
        :return:
        """
        result = self.session.scalars(select(WellData).where(WellData.id == id)).one_or_none()
        if result:
            return Well(q_liq=result.q_liq, p_wf=result.p_wf)
        return None

    def add(self, entity: Well):
        """
        Добавление данных
        :return:
        """
        self.session.add(WellData(id=entity.id, q_liq=entity.q_liq, p_wf=entity.p_wf))
        self.session.commit()
