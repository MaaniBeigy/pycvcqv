"""The types used in the package."""
# --------------------------- Import libraries and functions --------------------------
from typing import List, Tuple, TypeVar, Union

from multiprocessing import pool

import numpy as np
import pandas as pd
from numpy import typing as npt

# ---------------------------------- types definition ---------------------------------
ListFloat = List[float]
ListInt = List[int]
TupleFloat = Tuple[float]
TupleInt = Tuple[int]
ArrayFloat = npt.NDArray[np.float_]
ArrayInt = npt.NDArray[np.int_]
PoolType = TypeVar("PoolType", bound=pool.Pool)
NumArrayLike = TypeVar(
    "NumArrayLike",
    bound=Union[
        pd.Series, ArrayInt, ArrayFloat, ListFloat, ListInt, TupleFloat, TupleInt
    ],
)
