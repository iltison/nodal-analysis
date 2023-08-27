"""
Модуль содержит расчетный класс для построения IPR по обыкновенному Вогелю
"""
# thirdparty
import numpy as np


def calc_ipr(p_res: float, pi: float, wct: float, pb: float, points: int = 21) -> dict[str, list[float]]:
    """
    Расчет кривой IPR

    :param p_res: пластовое давление, атм
    :param pi: коэффициент продуктивности, м3/сут/атм
    :param wct: обводненность, %
    :param pb: давления насыщения, атм
    :param points: число точек
    """

    p_wf_list = np.linspace(1, p_res, points).tolist()

    q_inj_list = [calc_q_fluid(p_wf, pi, p_res, wct, pb) for p_wf in p_wf_list]

    result = {
        "p_wf": p_wf_list,
        "q_liq": q_inj_list,
    }

    return result


def calc_q_fluid(p_wf: float, pi: float, p_res: float, wct: float,
                 pb: float) -> float:
    """
    Расчет дебита жидкости по обыкновенному Вогелю

    Parameters
    ----------
    :param p_wf: забойное давление, атм
    :param pi: коэффициент продуктивности, м3/сут/атм
    :param p_res: пластовое давление, атм
    :param wct: обводненность, %
    :param pb: давления насыщения, атм

    :return: дебит жидкости, м3/сут
    -------
    """

    # вычисляем дебит при давлении равном давлению насыщения
    qb = pi * (p_res - pb)

    if wct == 100 or p_wf >= pb:
        return pi * (p_res - p_wf)

    fw = wct / 100
    fo = 1 - fw
    # максимальный дебит чистой нефти
    qo_max = qb + (pi * pb) / 1.8
    p_wfg = fw * (p_res - qo_max / pi)

    if p_wf > p_wfg:
        a = 1 + (p_wf - (fw * p_res)) / (0.125 * fo * pb)
        b = fw / (0.125 * fo * pb * pi)
        c = (2 * a * b) + 80 / (qo_max - qb)
        d = (a ** 2) - (80 * qb / (qo_max - qb)) - 81

        if b == 0:
            return abs(d / c)

        return (-c + ((c * c - 4 * b * b * d) ** 0.5)) / (2 * b ** 2)

    cg = 0.001 * qo_max
    cd = fw * (cg / pi) + fo * 0.125 * pb * (-1 + (1 + 80 *
                                                   ((0.001 * qo_max) /
                                                    (qo_max - qb))) ** 0.5)
    return (p_wfg - p_wf) / (cd / cg) + qo_max
