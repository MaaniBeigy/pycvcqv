"""The checkers traits."""

# --------------------------- Import libraries and functions --------------------------
import functools
import warnings

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


def is_ncp_huge(function):
    """
    A decorator function to check whether the noncentrality parameter exceeds 37.62.
    """

    # -------------------------------- wrapper function -------------------------------
    @functools.wraps(function)
    def wrapper(*args, **kw):
        """The wrapper function."""
        # ---------------------- declare noncentrality parameter ----------------------
        ncp = kw.get("ncp", args[0] if args else None)
        # ------------------- check noncentrality parameter is huge -------------------
        if ncp is not None and abs(ncp) > 37.62:
            warnings.warn(
                "The noncentrality parameter exceeds 37.62, which may affect accuracy.",
                RuntimeWarning,
                stacklevel=2,
            )
        return function(*args, **kw)

    # ------------------------------- return the wrapper ------------------------------
    return wrapper


def is_dof_positive_natural_number(function):
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
        if ("dof" in kw) and (not isinstance(kw["dof"], int) or kw["dof"] <= 0):
            # ----------------------- return the actual function ----------------------
            raise ValueError("Argument dof should be a positive natural number!")
        return function(*args, **kw)

    # ------------------------------- return the wrapper ------------------------------
    return wrapper


def validate_ncp_confidence_level_arguments(function):
    """Decorator to validate noncentrality parameter confidence interval arguments."""

    def wrapper(*args, **kwargs):
        """The wrapper function."""
        # ------------ Validate that conf_level is in the range [0, 1] ------------
        # ---------------- Extract the positional or keyword arguments ----------------
        conf_level = kwargs.get("conf_level", args[2] if len(args) > 2 else None)
        alpha_lower = kwargs.get("alpha_lower", args[3] if len(args) > 3 else None)
        alpha_upper = kwargs.get("alpha_upper", args[4] if len(args) > 4 else None)

        # --- If all three are None, use default conf_level and compute alpha values --
        if conf_level is None and alpha_lower is None and alpha_upper is None:
            conf_level = 0.95
            alpha_lower = (1 - conf_level) / 2
            alpha_upper = (1 - conf_level) / 2

        # ---- Calculate the alpha_lower and alpha_upper based on given conf_level ----
        elif conf_level is not None and alpha_lower is None and alpha_upper is None:
            alpha_lower = (1 - conf_level) / 2
            alpha_upper = (1 - conf_level) / 2

        # -- Validate if one of alpha_lower or alpha_upper is given, both must be given
        if (alpha_lower is not None) != (alpha_upper is not None):
            raise ValueError(
                "Both alpha_lower and alpha_upper must be provided or both None."
            )

        # --- Validate that alpha_lower and alpha_upper are within the [0, 1] range ---
        if alpha_lower is not None and not 0 <= alpha_lower <= 1:
            raise ValueError("conf_level or alpha values must be in the range [0, 1].")
        if alpha_upper is not None and not 0 <= alpha_upper <= 1:
            raise ValueError("conf_level or alpha values must be in the range [0, 1].")

        # --------------- Update the kwargs with validated alpha values ---------------
        kwargs.update(
            {
                "alpha_lower": alpha_lower,
                "alpha_upper": alpha_upper,
            }
        )

        return function(*args, **kwargs)

    # ------------------------------- return the wrapper ------------------------------
    return wrapper
