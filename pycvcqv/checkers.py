"""The checkers traits."""

# --------------------------- Import libraries and functions --------------------------
import functools

import pandas as pd
from pandas.api.types import is_numeric_dtype

# -------------------------------- function definition --------------------------------


def is_numeric(function):
    """A decorator function to check whether the input_vector is numeric."""

    # -------------------------------- wrapper function -------------------------------
    @functools.wraps(function)
    def wrapper(*args, **kw):
        """The wrapper function."""
        # ------------------------ if the **kwargs are not used -----------------------
        if len(kw) == 0 or "data" not in kw:
            # ------------------------------- DataFrame -------------------------------
            if isinstance(args[0], pd.DataFrame):
                return function(*args, **kw)
            # --------------------- if the 1st argument is numeric --------------------
            if is_numeric_dtype(pd.Series(args[0])):
                # --------------------- return the actual function --------------------
                return function(*args, **kw)
            raise TypeError("The data is not numeric!")
        # ------------------------- if the **kwargs include data ----------------------
        # --------------------------------- DataFrame ---------------------------------
        if isinstance(kw["data"], pd.DataFrame):
            return function(*args, **kw)
        # ----------------------- if the 1st argument is numeric ----------------------
        if is_numeric_dtype(pd.Series(kw["data"])):
            # ----------------------- return the actual function ----------------------
            return function(*args, **kw)
        raise TypeError("The data is not numeric!")

    # ------------------------------- return the wrapper ------------------------------
    return wrapper


def is_positive_natural_number(function):
    """A decorator function to check whether the input is a positive natural number."""

    # -------------------------------- wrapper function -------------------------------
    @functools.wraps(function)
    def wrapper(*args, **kw):
        """The wrapper function."""
        # ------------------------ if the **kwargs are not used -----------------------
        if len(kw) == 0 or "dof" not in kw:
            if not isinstance(args[1], int) or args[1] <= 0:
                raise ValueError("Argument dof should be a positive natural number!")
        # ------------------------- if the **kwargs include dof -----------------------
        if len(kw) != 0 and (not isinstance(kw["dof"], int) or kw["dof"]) <= 0:
            # ----------------------- return the actual function ----------------------
            raise ValueError("Argument dof should be a positive natural number!")
        return function(*args, **kw)

    # ------------------------------- return the wrapper ------------------------------
    return wrapper
