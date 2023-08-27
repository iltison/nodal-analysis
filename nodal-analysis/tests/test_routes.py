import numpy as np
import pytest


@pytest.mark.parametrize("test_input,expected", [
    (
            {"vlp": {
                "q_liq": [0, 30, 60, 90, 120, 150],
                "p_wf": [200, 190, 180, 175, 185, 200]
            },
                "ipr": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 180, 160, 140, 120, 100]
                }}, [{'p_wf': 200.0, 'q_liq': 0.0}]
    ),
    (
            {"vlp": {
                "q_liq": [0, 30, 60, 90, 120, 150],
                "p_wf": [200, 190, 180, 175, 185, 200]
            },
                "ipr": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 180, 160, 140, 120, 300]
                }}, [{'p_wf': 200.0, 'q_liq': 0.0}, {'p_wf': 190.91, 'q_liq': 131.82}]
    ),
(
            {"vlp": {
                "q_liq": [0, 30, 60, 90, 120, 150],
                "p_wf": [50, 50, 50, 50, 50, 50]
            },
                "ipr": {
                    "q_liq": [0, 30, 60, 90, 120, 150],
                    "p_wf": [200, 180, 160, 140, 120, 100]
                }}, []
    ),
(
            {"vlp": {
                "q_liq": [],
                "p_wf": []
            },
                "ipr": {
                    "q_liq": [],
                    "p_wf": []
                }}, []
    ),
])
def test_calc_model_success(api_client, test_input, expected):
    result = api_client.post('/nodal/calc', json=test_input)
    assert result.json() == expected
