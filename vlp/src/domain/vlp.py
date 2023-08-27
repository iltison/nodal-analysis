import hashlib
from dataclasses import dataclass, field, asdict


@dataclass
class Inclinometry:
    MD: list[int | float] = field(default_factory=list)
    TVD: list[int | float] = field(default_factory=list)


@dataclass
class Pipeline:
    diameter: float = field(default=0.0)


@dataclass
class Tubing:
    diameter: float = field(default=0.0)
    h_mes: int = field(default=0)


@dataclass
class PVT:
    wct: float = field(default=0.0)
    rp: float = field(default=0.0)
    gamma_oil: float = field(default=0.0)
    gamma_gas: float = field(default=0.0)
    gamma_wat: float = field(default=0.0)
    t_res: float = field(default=0.0)


@dataclass
class Vlp:
    inclinometry: Inclinometry
    casing: Pipeline
    tubing: Tubing
    pvt: PVT
    p_wh: float = field(default=0.0)
    geo_grad: float = field(default=0.0)
    h_res: float = field(default=0.0)

    id: str | None = None

    def set_hash_id(self):
        """
        Заполнение ид хешом
        :return:
        """
        data = str(asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
        hash_object = hashlib.md5(data.encode())
        self.id = hash_object.hexdigest()
