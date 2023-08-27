from typing import List

from pydantic import BaseModel, Field, confloat, validator, conint


class IprCalcRequest(BaseModel):
    p_res: confloat(gt=0) = Field(title="Пластовое давление, атм")
    wct: confloat(ge=0, le=100) = Field(title="Обводненность, %")
    pi: confloat(ge=0) = Field(title="Коэффициент продуктивности, м3/сут/атм")
    pb: confloat(ge=0) = Field(title="Давление насыщения, атм")
    points: conint(ge=0) = Field(title="Число точек", default=21)

    class Config:
        schema_extra = {
            "example": {
                "p_res": 250,
                "wct": 50,
                "pi": 1,
                "pb": 150,
                "points": 21,
            }
        }


class IprCalcResponse(BaseModel):
    q_liq: List[confloat(ge=0)] = Field(title="Дебиты жидкости, м3/сут")
    p_wf: List[confloat(gt=0)] = Field(title="Забойные давления, атм")

    @validator("q_liq", "p_wf")
    def round_result(cls, v):
        return [round(val, 2) for val in v]

    class Config:
        schema_extra = {
            "example": {
                "q_liq": [
                    190.04, 187.46, 184.87, 182.12, 177.57, 171.26, 163.59,
                    154.82, 145.13, 134.67, 123.53, 111.82, 99.60, 87.15,
                    74.70, 62.25, 49.80, 37.35, 24.90, 12.45, 0
                ],
                "p_wf": [
                    1, 13.45, 25.9, 38.34, 50.8, 63.25, 75.69, 88.14, 100.6,
                    113.05, 125.5, 137.95, 150.39, 162.85, 175.29, 187.75,
                    200.2, 212.64, 225.1, 237.54, 250
                ],
            }
        }
