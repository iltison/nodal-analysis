from shapely.geometry import LineString, MultiPoint, Point


def calc_nodal(vlp: dict, ipr: dict) -> list[dict[str, float]]:
    """
    Расчёт точки пересечения VLP vs IPR

    Parameters
    ----------
    vlp : dict
        Словарь, содержащий VLP
    ipr : dict
        Словарь, содержащий IPR
    """
    vlp_line = LineString(list(zip(vlp["q_liq"], vlp["p_wf"])))
    ipr_line = LineString(list(zip(ipr["q_liq"], ipr["p_wf"])))

    intersection = vlp_line.intersection(ipr_line)

    if isinstance(intersection, Point):
        return [{"p_wf": y, "q_liq": x} for x, y in intersection.coords]
    if isinstance(intersection, MultiPoint):
        print(intersection)
        return [{"p_wf": i.y, "q_liq": i.x} for i in intersection]
    return []
