"""true_input trait"""
# --------------------------- Import libraries and functions --------------------------

import numpy as np
import pandas as pd

# -------------------------------- function definition --------------------------------


def true_input(function):
    """decorator function to check whether the input_vector has correct type"""
    # -------------------------------- wrapper function -------------------------------
    def wrapper(*args, **kw):
        # ------------------------ if the **kwargs are not used -----------------------
        if len(kw) == 0 or "data" not in kw:
            # ------------ check if data is list, tuple, or array -----------
            if isinstance(args[0], (list, np.ndarray, pd.Series, tuple)):
                # --------------------- return the actual function --------------------
                return function(*args, **kw)
            raise TypeError(
                """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
            )
        # ------------------------ if the **kwargs include data -----------------------
        # ------------------- check if data is list, tuple, or array ------------------
        if isinstance(kw["data"], (list, np.ndarray, pd.Series, tuple)):
            # ----------------------- return the actual function ----------------------
            return function(*args, **kw)
        raise TypeError(
            """data must be \
pandas.core.series.Series, numpy.ndarray, list, or tuple!"""
        )

    # ------------------------------- return the wrapper ------------------------------
    return wrapper
