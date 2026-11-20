import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.fixture
def runner():
    return CliRunner()

# region CLEAN
def test_clean_remove_command(runner):
    result = runner.invoke(cli, ["clean", "remove", "1", "nan", "3.5", "abc"])
    assert result.exit_code == 0
    assert result.output.strip() == "[1.0, 3.5]"


@pytest.mark.parametrize(
    "args, expected",
    [
        (["1", "2", "3"], "[1.0, 2.0, 3.0]"),
        (["nan"], "[]"),
        (["nan", "4"], "[4.0]"),
        (["x", "y", "2.5"], "[2.5]"),
    ],
)
def test_clean_remove_parametrized(runner, args, expected):
    result = runner.invoke(cli, ["clean", "remove", *args])
    assert result.exit_code == 0
    assert result.output.strip() == expected


def test_clean_fill_default(runner):
    result = runner.invoke(cli, ["clean", "fill", "1", "nan", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "[1.0, 0.0, 3.0]"


@pytest.mark.parametrize(
    "option, fill_value, expected",
    [
        ("--fill-value", "5", "[1.0, 5.0, 3.0]"),
        ("--fill-value", "-1.5", "[1.0, -1.5, 3.0]"),
        ("--fill-value", "0", "[1.0, 0.0, 3.0]"),
    ],
)
def test_clean_fill_with_option(runner, option, fill_value, expected):
    result = runner.invoke(cli, ["clean", "fill", option, fill_value, "1", "nan", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == expected


def test_clean_fill_invalid_option_value(runner):
    result = runner.invoke(cli, ["clean", "fill", "--fill-value", "abc", "1", "nan"])
    assert result.exit_code != 0
    assert "Invalid value" in result.output


def test_clean_group_help_lists_commands(runner):
    result = runner.invoke(cli, ["clean", "--help"])
    assert result.exit_code == 0
    assert "remove" in result.output
    assert "fill" in result.output


# endregion
