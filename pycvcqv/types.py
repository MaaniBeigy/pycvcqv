"""The types used in the package."""

# --------------------------- Import libraries and functions --------------------------
from typing import Callable, List, Optional, Tuple, TypeVar, Union

from multiprocessing import pool

import numpy as np
import pandas as pd
from numpy import typing as npt

# ---------------------------------- types definition ---------------------------------
ListFloat = List[float]
ListInt = List[int]
TupleFloat = Tuple[float]
TupleInt = Tuple[int]
ArrayFloat = npt.NDArray[np.float64]
ArrayInt = npt.NDArray[np.int_]
PoolTypeT = TypeVar("PoolTypeT", bound=pool.Pool)
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
        Optional[int],
        Optional[int],
        Optional[bool],
        Optional[int],
        Optional[bool],
        Optional[int],
        Optional[float],
        Optional[float],
        Optional[float],
        Optional[float],
        Optional[int],
    ],
    pd.DataFrame,
]
