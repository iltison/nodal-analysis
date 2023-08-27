from typing import List

from pydantic import BaseModel, Field, confloat, validator


class VlpIprCalcResponse(BaseModel):
    q_liq: List[confloat(ge=0)] = Field(title="Дебиты жидкости, м3/сут")
    p_wf: List[confloat(gt=0)] = Field(title="Забойные давления, атм")


class NodalCalcRequest(BaseModel):
    ipr: VlpIprCalcResponse = Field(title="IPR")
    vlp: VlpIprCalcResponse = Field(title="VLP")

    class Config:
        schema_extra = {
            "example": {
                "vlp": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 190, 180, 175, 185, 200]
                },
                "ipr": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 180, 160, 140, 120, 100]
                }
            }
        }


class NodalCalcDecision(BaseModel):
    p_wf: confloat(gt=0) = Field(title="Забойное давление, атм")
    q_liq: confloat(ge=0) = Field(title="Дебит жидкости, м3/сут")

    @validator("q_liq", "p_wf")
    def round_result(cls, v):
        return round(v, 2)


class NodalCalcResponse(BaseModel):
    __root__: List[NodalCalcDecision]

    class Config:
        schema_extra = {"example": [{"p_wf": 200, "q_liq": 0}]}
