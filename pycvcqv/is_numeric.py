"""is_numeric trait"""
# --------------------------- Import libraries and functions --------------------------

import pandas as pd
from pandas.api.types import is_numeric_dtype

# -------------------------------- function definition --------------------------------


def is_numeric(function):
    """a decorator function to check whether the input_vector is numeric"""
    # -------------------------------- wrapper function -------------------------------
    def wrapper(*args, **kw):
        # ------------------------ if the **kwargs are not used -----------------------
        if len(kw) == 0 or "numeric_vector" not in kw:
            # --------------------- if the 1st argument is numeric --------------------
            if is_numeric_dtype(pd.Series(args[0])):
                # --------------------- return the actual function --------------------
                return function(*args, **kw)
            raise TypeError("The vector is not numeric!")
        # ------------------- if the **kwargs include numeric_vector ------------------
        # ----------------------- if the 1st argument is numeric ----------------------
        if is_numeric_dtype(pd.Series(kw["numeric_vector"])):
            # ----------------------- return the actual function ----------------------
            return function(*args, **kw)
        raise TypeError("The vector is not numeric!")

    # ------------------------------- return the wrapper ------------------------------
    return wrapper
