import json

import click

import src.preprocessing as preprocessing


def _to_float_or_nan(value: str) -> float:
    """Converts a string to float; anything that is not a number becomes NaN."""
    try:
        return float(value)
    except ValueError:
        return float("nan")


@click.group()
def cli():
    """General group of the preprocessing command line interface."""


# region CLEAN
@cli.group()
def clean():
    """Functions related to data cleaning."""


@clean.command("remove")
@click.argument("values", nargs=-1)
def remove_missing_values(values):
    l_values = [_to_float_or_nan(v) for v in values]
    click.echo(preprocessing.remove_missing_values(l_values))


@clean.command("fill")
@click.argument("values", nargs=-1)
@click.option(
    "--fill-value",
    type=float,
    default=0,
    show_default=True,
    help="Value used to replace the missing values.",
)
def filling_missing_values(values, fill_value):
    l_values = [_to_float_or_nan(v) for v in values]
    click.echo(preprocessing.filling_missing_values(l_values, fill_value))


# endregion


# region NUMERIC
@cli.group()
def numeric():
    """Functions related to numerical attributes."""


@numeric.command("normalize")
@click.argument("values", nargs=-1, type=float)
@click.option(
    "--new-min",
    type=float,
    default=0,
    show_default=True,
    help="Minimum value of the new range.",
)
@click.option(
    "--new-max",
    type=float,
    default=1,
    show_default=True,
    help="Maximum value of the new range.",
)
def normalize(values, new_min, new_max):
    click.echo(preprocessing.normalization_min_max(list(values), new_min, new_max))


@numeric.command("standardize")
@click.argument("values", nargs=-1, type=float)
def standardize(values):
    click.echo(preprocessing.standarization_z_score(list(values)))


@numeric.command("clip")
@click.argument("values", nargs=-1, type=float)
@click.option(
    "--lower",
    type=float,
    default=0,
    show_default=True,
    help="Minimum value to clip to.",
)
@click.option(
    "--upper",
    type=float,
    default=1,
    show_default=True,
    help="Maximum value to clip to.",
)
def clip(values, lower, upper):
    click.echo(preprocessing.clipping_values(list(values), lower, upper))


@numeric.command("to-int")
@click.argument("values", nargs=-1)
def conversion_to_integers(values):
    click.echo(preprocessing.conversion_to_integers(list(values)))


@numeric.command("log")
@click.argument("values", nargs=-1, type=float)
def log_scale_transformation(values):
    click.echo(preprocessing.log_scale_transformation(list(values)))


# endregion


# region TEXT
@cli.group()
def text():
    """Functions related to textual information."""


@text.command("tokenize")
@click.argument("txt")
def tokenization(txt):
    click.echo(preprocessing.tokenization_alphanumeric_lower_casing(txt))


@text.command("remove-punctuation")
@click.argument("txt")
def remove_punctuation(txt):
    click.echo(preprocessing.selection_alphanumerical_spaces(txt))


@text.command("remove-stop-words")
@click.argument("txt")
@click.option(
    "--stop-words", "-s", multiple=True, help="Stop word to remove. Can be repeated."
)
def remove_stop_words(txt, stop_words):
    click.echo(preprocessing.remove_stop_words(txt, [w.lower() for w in stop_words]))


# endregion


# region STRUCT
@cli.group()
def struct():
    """Functions related to the structure of data."""


@struct.command("shuffle")
@click.argument("values", nargs=-1)
@click.option(
    "--seed",
    type=int,
    default=None,
    show_default=True,
    help="Integer seed to make the shuffle reproducible.",
)
def shuffle(values, seed):
    click.echo(preprocessing.shuffle_list(list(values), seed))


@struct.command("flatten")
@click.argument("matrix")
def flatten(matrix):
    try:
        l_l_values = json.loads(matrix)
    except json.JSONDecodeError as exc:
        raise click.BadParameter("it must be a valid JSON list of lists.") from exc
    click.echo(preprocessing.flatten_matrix(l_l_values))


@struct.command("unique")
@click.argument("values", nargs=-1)
def unique_values(values):
    click.echo(preprocessing.remove_duplicated_values(list(values)))


# endregion


if __name__ == "__main__":
    cli()
