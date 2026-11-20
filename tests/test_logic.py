"""Integration tests for the preprocessing logic."""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring


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


# region NUMERICAL TRANSFORMATION
def test_remove_duplicated_values():
    assert sorted(preprocessing.remove_duplicated_values([3, 1, 3, 2, 1])) == [1, 2, 3]


@pytest.mark.parametrize(
    "l_values, new_min, new_max, expected",
    [
        ([1.0, 2.0, 3.0], 0.0, 1.0, [0.0, 0.5, 1.0]),
        ([1.0, 2.0, 3.0], 10.0, 20.0, [10.0, 15.0, 20.0]),
        ([5.0, 5.0], 0.0, 1.0, [0.0, 0.0]),
        ([], 0.0, 1.0, []),
    ],
)
def test_normalization_min_max(l_values, new_min, new_max, expected):
    assert preprocessing.normalization_min_max(l_values, new_min, new_max) == expected


def test_standarization_z_score_mean_zero():
    result = preprocessing.standarization_z_score([1.0, 2.0, 3.0, 4.0])
    assert sum(result) == pytest.approx(0.0)


def test_standarization_z_score_constant():
    assert preprocessing.standarization_z_score([2.0, 2.0]) == [0.0, 0.0]


def test_standarization_z_score_empty():
    assert preprocessing.standarization_z_score([]) == []


@pytest.mark.parametrize(
    "lower, upper, expected",
    [
        (0.0, 1.0, [0.0, 0.5, 1.0]),
        (1.0, 2.0, [1.0, 1.0, 2.0]),
    ],
)
def test_clipping_values(lower, upper, expected):
    assert preprocessing.clipping_values([-1.0, 0.5, 3.0], lower, upper) == expected


def test_conversion_to_integers_ignores_non_numeric():
    assert preprocessing.conversion_to_integers(["1", "a", "22"]) == [1, 22]


def test_log_scale_transformation():
    assert preprocessing.log_scale_transformation([1.0, math.e]) == pytest.approx(
        [0.0, 1.0]
    )


# endregion


# region TEXT
@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Hello, World!", "hello world"),
        ("snake_case 42", "snake case 42"),
        ("No punctuation here", "no punctuation here"),
        ("", ""),
    ],
)
def test_tokenization_alphanumeric_lower_casing(txt, expected):
    assert preprocessing.tokenization_alphanumeric_lower_casing(txt) == expected


def test_selection_alphanumerical_spaces():
    assert (
        preprocessing.selection_alphanumerical_spaces("Hello, World!") == "Hello World"
    )


def test_remove_stop_words():
    assert (
        preprocessing.remove_stop_words("The cat and dog", ["the", "and"]) == "cat dog"
    )


# endregion


# region STRUCT
def test_flatten_matrix():
    assert preprocessing.flatten_matrix([[1, 2], [3], []]) == [1, 2, 3]


def test_shuffle_list_same_elements_and_seed_reproducible():
    first = preprocessing.shuffle_list(list(range(10)), seed=1)
    second = preprocessing.shuffle_list(list(range(10)), seed=1)
    assert first == second
    assert sorted(first) == list(range(10))


# endregion
