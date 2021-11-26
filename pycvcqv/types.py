"""The types used in the package."""
# --------------------------- Import libraries and functions --------------------------
from typing import List, Tuple, TypeVar

from multiprocessing import pool

import numpy as np
from numpy import typing as npt

# ---------------------------------- types definition ---------------------------------
ListFloat = List[float]
ListInt = List[int]
TupleFloat = Tuple[float]
TupleInt = Tuple[int]
ArrayFloat = npt.NDArray[np.float_]
ArrayInt = npt.NDArray[np.int_]
PoolType = TypeVar("PoolType", bound=pool.Pool)
