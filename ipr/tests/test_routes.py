import pytest


@pytest.mark.parametrize("test_input,expected", [
    (
            {
                "p_res": 250,
                "wct": 50,
                "pi": 1,
                "pb": 150,
                "points": 21,
            },
            {'p_wf': [1.0, 13.45, 25.9, 38.35, 50.8, 63.25, 75.7, 88.15, 100.6, 113.05, 125.5, 137.95, 150.4, 162.85,
                      175.3, 187.75, 200.2, 212.65, 225.1, 237.55, 250.0],
             'q_liq': [190.04, 187.46, 184.88, 182.12, 177.57, 171.27, 163.6, 154.82, 145.13, 134.67, 123.54, 111.83,
                       99.6, 87.15, 74.7, 62.25, 49.8, 37.35, 24.9, 12.45, 0.0]}
    ),
    (
            {
                "p_res": 200,
                "wct": 50,
                "pi": 1,
                "pb": 150,
                "points": 6
            },
            {'p_wf': [1.0, 40.8, 80.6, 120.4, 160.2, 200.0],
             'q_liq': [139.98, 131.39, 110.26, 78.17, 39.8, 0.0]}
    ),
])
def test_calc_model_success(api_client, test_input, expected):
    result = api_client.post('/ipr/calc', json=test_input)
    assert result.json() == expected
