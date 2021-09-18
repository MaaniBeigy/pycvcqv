"""types used in the package"""
# --------------------------- Import libraries and functions --------------------------
from typing import Any, Callable, List, Tuple, TypeVar

import numpy as np
import numpy.typing as npt

# ---------------------------------- types definition ---------------------------------
ListFloat = List[float]
ListInt = List[int]
TupleFloat = Tuple[float]
TupleInt = Tuple[int]
ArrayFloat = npt.NDArray[np.float_]
ArrayInt = npt.NDArray[np.int_]
FunctionType = TypeVar("FunctionType", bound=Callable[..., Any])
