from dataclasses import dataclass, field


@dataclass
class Well:
    q_liq: list[float] = field(default_factory=list)
    p_wf: list[float] = field(default_factory=list)
    id: str | None = None
