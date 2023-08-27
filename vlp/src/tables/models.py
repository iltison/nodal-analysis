import sqlalchemy as sa

from src.infrastructures.db import Base


class WellData(Base):
    __tablename__ = "well_data"
    id = sa.Column(sa.String, primary_key=True, index=True, nullable=False, comment="Идентификатор")
    q_liq = sa.Column(sa.ARRAY(sa.Float), comment="Дебиты жидкости, м3/сут")
    p_wf = sa.Column(sa.ARRAY(sa.Float), comment="Забойное давление, атм")


class VLPModel(Base):
    __tablename__ = "vlp"
    id = sa.Column(sa.String, primary_key=True, index=True, nullable=False, comment="Идентификатор")
    md = sa.Column(sa.ARRAY(sa.Float), comment="Измеренная по стволу глубина, м")
    tvd = sa.Column(sa.ARRAY(sa.Float), comment="Вертикальная глубина, м")
    casing_d = sa.Column(sa.Float, comment="Данные по ЭК. Диаметр трубы, м")
    tubing_d = sa.Column(sa.Float, comment="Данные по НКТ. Диаметр трубы, м")
    tubing_h_mes = sa.Column(sa.Float, comment="Данные по НКТ. Глубина спуска НКТ, м")
    pvt_wct = sa.Column(sa.Float, comment="PVT. Обводненность, %")
    pvt_rp = sa.Column(sa.Float, comment="PVT. Газовый фактор, м3/т")
    pvt_gamma_oil = sa.Column(sa.Float, comment="PVT. Отн. плотность нефти")
    pvt_gamma_gas = sa.Column(sa.Float, comment="PVT. Отн. плотность газа")
    pvt_gamma_wat = sa.Column(sa.Float, comment="PVT. Отн. плотность воды")
    pvt_t_res = sa.Column(sa.Float, comment="PVT. Пластовая температура, C")
    p_wh = sa.Column(sa.Float, comment="Буферное давление, атм")
    geo_grad = sa.Column(sa.Float, comment="Градиент температуры, C/100 м")
    h_res = sa.Column(sa.Float, comment="Глубина Верхних Дыр Перфорации, м")
