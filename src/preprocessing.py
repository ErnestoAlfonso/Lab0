import math
import re
import random


# region CLEANING
def remove_missing_values(l_values: list[float]) -> list[float]:
    """
    Removes missing values (NaN) from a list of float values.

    Args:
        l_values (List[float]): A list of float values that may contain NaN.
    """
    l_values = [
        value for value in l_values if isinstance(value, float) and (value == value)
    ]
    return l_values


def filling_missing_values(
    l_values: list[float], fill_value: float = 0.0
) -> list[float]:
    """
    Fills missing values (NaN) in a list of float values with a specified fill value.

    Args:
        l_values (List[float]): A list of float values that may contain NaN.
        fill_value (float): The value to replace NaN with.
    """
    l_values = [
        value if isinstance(value, float) and (value == value) else fill_value
        for value in l_values
    ]
    return l_values


# endregion


# region NUMERICAL TRANSFORMATION
def remove_duplicated_values(l_values: list[float]) -> list[float]:
    """
    Removes duplicated values from a list of float values.

    Args:
        l_values (List[float]): A list of float values that may contain duplicates.
    """
    l_values = list(set(l_values))
    return l_values


def normalization_min_max(
    l_values: list[float], new_min: float = 0.0, new_max: float = 1.0
) -> list[float]:
    """
    Normalizes a list of float values using min-max normalization.

    Args:
        l_values (List[float]): A list of float values to be normalized.
        new_min (float): Minimum value of the new range.
        new_max (float): Maximum value of the new range.
    """
    if not l_values:
        return l_values
    min_val = min(l_values)
    max_val = max(l_values)
    if min_val == max_val:
        return [new_min] * len(l_values)
    scale = (new_max - new_min) / (max_val - min_val)
    return [new_min + (value - min_val) * scale for value in l_values]


def standarization_z_score(l_values: list[float]) -> list[float]:
    """
    Standardizes a list of float values using z-score standardization.

    Args:
        l_values (List[float]): A list of float values to be standardized.
    """
    if not l_values:
        return l_values
    mean = sum(l_values) / len(l_values)
    squared_diffs = [(value - mean) ** 2 for value in l_values]
    variance = sum(squared_diffs) / len(l_values)
    std_dev = variance**0.5
    if std_dev == 0:
        return [0.0] * len(l_values)
    return [(value - mean) / std_dev for value in l_values]


def clipping_values(
    l_values: list[float], lower_bound: float = 0.0, upper_bound: float = 1.0
) -> list[float]:
    """
    Clips values in a list of float values to a specified range.

    Args:
        l_values (List[float]): A list of float values to be clipped.
        lower_bound (float): The lower bound for clipping.
        upper_bound (float): The upper bound for clipping.
    """
    return [max(lower_bound, min(upper_bound, value)) for value in l_values]


def conversion_to_integers(l_values: list[str]) -> list[int]:
    """
    Converts a list of str values to integers. Excluded non-nnumerical values from the output

    Args:
        l_values (List[float]): A list of float values to be converted.
    """
    l_values = [item for item in l_values if item.isdigit()]
    return [int(item) for item in l_values]


def log_scale_transformation(l_values: list[float]):
    l_values = [math.log(value) for value in l_values]
    return l_values


# endregion


# region TEXT
def tokenization_alphanumeric_lower_casing(txt: str) -> str:
    """
    Tokenizes a text into words, keeping only alphanumeric characters and
    lower casing them.

    Args:
        txt (str): Text to be processed.

    Returns:
        str: Processed text, with the lower-cased words separated by single spaces.
    """
    words = re.findall(r"[^\W_]+", txt)
    return " ".join(word.lower() for word in words)


def selection_alphanumerical_spaces(txt: str) -> str:
    """ """
    return re.sub(r"[^a-zA-Z0-9\s]", "", txt)


def remove_stop_words(txt: str, stop_words: list[str]) -> str:
    """ """
    words = txt.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)


# endregion


# region STRUCT
def flatten_matrix(l_l_values: list[list]) -> list:
    """ """
    return [item for sublist in l_l_values for item in sublist]


def shuffle_list(l_values: list[float], seed: int | None = None) -> list[float]:
    """ """
    random.seed(seed)
    random.shuffle(l_values)
    return l_values


# endregion
