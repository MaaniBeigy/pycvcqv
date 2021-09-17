"""types used in the package"""
# --------------------------- Import libraries and functions --------------------------
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

# ---------------------------------- types definition ---------------------------------
ListFloat = List[float]
ListInt = List[int]
TupleFloat = Tuple[float]
TupleInt = Tuple[int]
ArrayFloat = npt.NDArray[np.float_]
ArrayInt = npt.NDArray[np.int_]
