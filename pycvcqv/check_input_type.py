"""true_input trait"""
# ------------------------ Import libraries and functions ---------------------

import numpy as np
import pandas as pd

# ---------------------------- function definition ----------------------------


def true_input(function):
    """decorator function to check whether the input_vector has correct type"""
    # ---------------------------- wrapper function ---------------------------
    def wrapper(*args, **kw):
        # -------------------- if the **kwargs are not used -------------------
        if len(kw) == 0 or "numeric_vector" not in kw:
            # -------- check if numeric_vector is list, tuple, or array -------
            if (
                isinstance(args[0], list)
                or isinstance(args[0], tuple)
                or isinstance(args[0], np.ndarray)
                or isinstance(args[0], pd.Series)
            ):
                # --------------- return the actual function --------------
                return function(*args, **kw)
            else:
                raise TypeError(
                    """numeric_vector must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
                )
        # --------------- if the **kwargs include numeric_vector --------------
        else:
            # -------- check if numeric_vector is list, tuple, or array -------
            if (
                isinstance(kw["numeric_vector"], list)
                or isinstance(kw["numeric_vector"], tuple)
                or isinstance(kw["numeric_vector"], np.ndarray)
                or isinstance(kw["numeric_vector"], pd.Series)
            ):
                # --------------- return the actual function --------------
                return function(*args, **kw)
            else:
                raise TypeError(
                    """numeric_vector must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
                )

    # --------------------------- return the wrapper --------------------------
    return wrapper
