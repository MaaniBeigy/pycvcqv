"""handle_nan trait"""
# --------------------------- Import libraries and functions --------------------------
import pandas as pd


# -------------------------------- function definition --------------------------------
def handle_nan(function):
    """a decorator function to handle nan"""
    # -------------------------------- wrapper function -------------------------------
    def wrapper(*args, **kw):
        # ---------------------------- no keyword arguments ---------------------------
        if len(kw) == 0:
            # -------------------------- check zero quantiles -------------------------
            if (
                pd.Series(args[0]).quantile(0.25) + pd.Series(args[0]).quantile(0.75)
            ) == 0:
                # --------------------------- raise warning ---------------------------
                raise Warning("cqv is NaN because q3 and q1 are 0")
            # ----------------------- return the actual function ----------------------
            return function(*args, **kw)
        # --------------------------- with keyword arguments --------------------------
        if len(kw) != 0 and "data" in kw:
            # -------------------------- check zero quantiles -------------------------
            if (
                pd.Series(kw["data"]).quantile(0.25)
                + pd.Series(kw["data"]).quantile(0.75)
            ) == 0:
                # --------------------------- raise warning ---------------------------
                raise Warning("cqv is NaN because q3 and q1 are 0")
            # ----------------------- return the actual function ----------------------
            return function(*args, **kw)
        # ------------------------------ other situations -----------------------------
        if (pd.Series(args[0]).quantile(0.25) + pd.Series(args[0]).quantile(0.75)) == 0:
            raise Warning("cqv is NaN because q3 and q1 are 0")
        # ------------------------- return the actual function ------------------------
        return function(*args, **kw)

    # ------------------------------- return the wrapper ------------------------------
    return wrapper
