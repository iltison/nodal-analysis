import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.domain.vlp import Vlp, Inclinometry, Pipeline, Tubing, PVT
from src.domain.well import Well
from src.infrastructures.vlp_repository import VlpRepositoryProtocol
from src.infrastructures.well_repository import WellRepositoryProtocol
from src.routes.vlp import main_router

app = FastAPI()
app.include_router(main_router)
client = TestClient(app)


def generate_excepted_date_for_tests() -> dict:
    excepted = {'q_liq': [0.0, 66.67, 133.33, 200.0, 266.67, 333.33, 400.0],
                'p_wf': [41.13, 17.75, 20.4, 27.31, 36.94, 48.67, 62.29]}
    return excepted


def generate_data_for_tests() -> dict:
    data = {
        "inclinometry": {
            "MD": [
                0.0,
                1000.0,
                1500.0
            ],
            "TVD": [
                0.0,
                1000.0,
                1100.0
            ]
        },
        "casing": {
            "d": 0.1
        },
        "tubing": {
            "d": 0.062,
            "h_mes": 1000.0
        },
        "pvt": {
            "wct": 50.0,
            "rp": 100.0,
            "gamma_oil": 0.8,
            "gamma_gas": 0.7,
            "gamma_wat": 1.0,
            "t_res": 90.0
        },
        "p_wh": 10.0,
        "geo_grad": 3.0,
        "h_res": 1500.0
    }

    return data

def factory_vlp():
    gen_data = generate_data_for_tests()
    vlp = Vlp(inclinometry=Inclinometry(MD=gen_data['inclinometry']['MD'],
                                        TVD=gen_data['inclinometry']['TVD']),
              casing=Pipeline(diameter=gen_data['casing']['d']),
              tubing=Tubing(diameter=gen_data['tubing']['d'],
                            h_mes=gen_data['tubing']['h_mes']),
              pvt=PVT(wct=gen_data['pvt']['wct'],
                      rp=gen_data['pvt']['rp'],
                      gamma_oil=gen_data['pvt']['gamma_oil'],
                      gamma_gas=gen_data['pvt']['gamma_gas'],
                      gamma_wat=gen_data['pvt']['gamma_wat'],
                      t_res=gen_data['pvt']['t_res'], ),
              p_wh=gen_data['p_wh'],
              geo_grad=gen_data['geo_grad'],
              h_res=gen_data['h_res'],
              )
    vlp.set_hash_id()
    return vlp

def factory_well():
    exc_data = generate_excepted_date_for_tests()
    vlp = factory_vlp()
    return Well(q_liq=exc_data["q_liq"], p_wf=exc_data["p_wf"], id=vlp.id)

class FakeVlpRepository(VlpRepositoryProtocol):
    def __init__(self):
        self.payload = {}
        self.count_added = 0

    def add(self, entity):
        self.payload[entity.id] = entity
        self.count_added += 1

    def get(self, id: str) -> Vlp | None:
        if res := self.payload.get(id):
            return res
        return None


class FakeWellRepository(WellRepositoryProtocol):
    def __init__(self):
        self.payload = {}
        self.count_added = 0

    def get(self, id: str) -> Well | None:
        if res:=self.payload.get(id):
            return res
        return None

    def add(self, entity: Well):
        self.payload[entity.id] = entity
        self.count_added += 1


def test_with_cache():
    fake_well_repo = FakeWellRepository()
    fake_vlp_repo = FakeVlpRepository()
    app.dependency_overrides[VlpRepositoryProtocol] = lambda: fake_vlp_repo
    app.dependency_overrides[WellRepositoryProtocol] = lambda: fake_well_repo

    well = factory_well()
    vlp = factory_vlp()
    fake_well_repo.payload[well.id] = well
    fake_vlp_repo.payload[vlp.id] = vlp

    result = client.post('/vlp/calc', json=generate_data_for_tests())

    assert result.json() == generate_excepted_date_for_tests()

    assert fake_well_repo.payload[well.id] == well
    assert fake_well_repo.count_added == 0

    assert fake_vlp_repo.payload[vlp.id] == vlp
    assert fake_vlp_repo.count_added == 0

def test_without_cache():
    fake_well_repo = FakeWellRepository()
    fake_vlp_repo = FakeVlpRepository()
    app.dependency_overrides[VlpRepositoryProtocol] = lambda: fake_vlp_repo
    app.dependency_overrides[WellRepositoryProtocol] = lambda: fake_well_repo

    result = client.post('/vlp/calc', json=generate_data_for_tests())

    assert result.json() == generate_excepted_date_for_tests()

    assert fake_well_repo.count_added == 1

    assert fake_vlp_repo.count_added == 1
