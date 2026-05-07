"""The types used in the package."""

# --------------------------- Import libraries and functions --------------------------
from typing import TypeVar, Union

from collections.abc import Callable
from multiprocessing import pool

import numpy as np
import pandas as pd
from numpy import typing as npt

# ---------------------------------- types definition ---------------------------------
ListFloat = list[float]
ListInt = list[int]
TupleFloat = tuple[float]
TupleInt = tuple[int]
ArrayFloat = npt.NDArray[np.float64]
ArrayInt = npt.NDArray[np.int_]
PoolTypeT = TypeVar("PoolTypeT", bound=pool.Pool)
# `Union` is required here (not `X | Y`) because TypeVar(bound=...) needs a
# concrete type expression — PEP 604 unions inside `bound=` are evaluated as
# `types.UnionType`, which TypeVar accepts on 3.11+ but older type-checkers
# still struggle with.
NumArrayLike = TypeVar(
    "NumArrayLike",
    bound=Union[
        pd.Series, ArrayInt, ArrayFloat, ListFloat, ListInt, TupleFloat, TupleInt
    ],
)
CvProcessor = Callable[
    [
        pd.DataFrame,
        str,
        int | None,
        int | None,
        bool | None,
        int | None,
        bool | None,
        int | None,
        float | None,
        float | None,
        float | None,
        float | None,
        int | None,
        int | None,
        int | np.random.Generator | None,
    ],
    pd.DataFrame,
]
CqvProcessor = Callable[
    [
        pd.DataFrame,
        str | None,
        int | None,
        str | None,
        int | None,
        int | None,
        bool | None,
        float | None,
        float | None,
        float | None,
        int | None,
        int | np.random.Generator | None,
    ],
    pd.DataFrame,
]
