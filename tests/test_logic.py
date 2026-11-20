import math

import pytest

import src.preprocessing as preprocessing


# region FIXTURES
@pytest.fixture
def values_with_nan():
    return [1.0, float("nan"), 3.5, float("nan"), -2.0]


# endregion


# region CLEANING
def test_remove_missing_values_removes_nan(values_with_nan):
    assert preprocessing.remove_missing_values(values_with_nan) == [1.0, 3.5, -2.0]


def test_remove_missing_values_does_not_leave_nan(values_with_nan):
    result = preprocessing.remove_missing_values(values_with_nan)
    assert not any(math.isnan(v) for v in result)


@pytest.mark.parametrize(
    "l_values, expected",
    [
        ([], []),
        ([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]),
        ([float("nan")], []),
        ([float("nan"), 4.0], [4.0]),
        ([1.0, "a", None, 2.0], [1.0, 2.0]),
    ],
)
def test_remove_missing_values_parametrized(l_values, expected):
    assert preprocessing.remove_missing_values(l_values) == expected


def test_filling_missing_values_default_fill(values_with_nan):
    assert preprocessing.filling_missing_values(values_with_nan) == [
        1.0,
        0.0,
        3.5,
        0.0,
        -2.0,
    ]


def test_filling_missing_values_keeps_length(values_with_nan):
    assert len(preprocessing.filling_missing_values(values_with_nan, 9.0)) == len(
        values_with_nan
    )


@pytest.mark.parametrize(
    "l_values, fill_value, expected",
    [
        ([], 0.0, []),
        ([1.0, 2.0], 5.0, [1.0, 2.0]),
        ([float("nan"), 2.0], 5.0, [5.0, 2.0]),
        ([float("nan"), float("nan")], -1.5, [-1.5, -1.5]),
        ([1.0, None, "x"], 7.0, [1.0, 7.0, 7.0]),
    ],
)
def test_filling_missing_values_parametrized(l_values, fill_value, expected):
    assert preprocessing.filling_missing_values(l_values, fill_value) == expected


# endregion
