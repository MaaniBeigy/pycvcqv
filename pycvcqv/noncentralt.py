"""Noncentral t-distribution module."""

# --------------------------- Import libraries and functions --------------------------
from typing import Dict, Optional, Union

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import nct

from pycvcqv.checkers import is_dof_positive_natural_number, is_ncp_huge
from pycvcqv.sanitizers import validate_ncp_confidence_level_arguments


# -------------------------------- function definition --------------------------------
@is_dof_positive_natural_number
@is_ncp_huge
@validate_ncp_confidence_level_arguments
def conf_limits_nct_minimize_scalar(
    ncp: float,
    dof: int,
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
    tol: Optional[float] = 1e-9,
    max_iter: Optional[int] = 10000,
) -> Dict[str, Union[float, int]]:
    """
    Calculate confidence limits for the noncentrality parameter (NCP) of the
    noncentral t-distribution using scipy.optimize.minimize_scalar.

    This function uses the scipy.optimize.minimize_scalar method to estimate
    the lower and upper confidence limits for the noncentrality
    parameter (NCP) given the degrees of freedom, confidence level, and other parameters.

    Args:
        ncp (float): The observed noncentrality parameter. Can be passed as 't_value'.
        dof (int): Degrees of freedom. Must be positive.
        conf_level (float, optional): The confidence level for the interval.
        alpha_lower (float, optional): The significance level for the lower tail.
        alpha_upper (float, optional): The significance level for the upper tail.
        tol (float, optional): Tolerance for the optimization algorithms. Default is 1e-9.
        max_iter (int, optional): Maximum number of iterations to perform. Default is 10000.

    Returns:
        dict: A dictionary with the following keys:
            - lower_limit (float): Lower confidence limit for the NCP.
            - prob_less_lower (float): Probability that the NCP is less than the lower limit.
            - upper_limit (float): Upper confidence limit for the NCP.
            - prob_greater_upper (float): Probability that the NCP is greater than the upper limit.

    Example:
        .. code:: python
            >>> conf_limits_nct_minimize_scalar(ncp=2.83, dof=126, conf_level=0.95)
            ...     {
            ...     'lower_limit': 0.8337502600175457,
            ...     'prob_less_lower': 0.02499999995262825,
            ...     'upper_limit': 4.815359140504376,
            ...     'prob_greater_upper': 0.024999999971943743
            ...     }
    """
    # --- If all three are None, use default conf_level and compute alpha values --
    if conf_level is None and alpha_lower is None and alpha_upper is None:
        conf_level = 0.95
        alpha_lower = (1 - conf_level) / 2
        alpha_upper = (1 - conf_level) / 2
    # ---- Calculate the alpha_lower and alpha_upper based on given conf_level ----
    elif conf_level is not None and alpha_lower is None and alpha_upper is None:
        alpha_lower = (1 - conf_level) / 2
        alpha_upper = (1 - conf_level) / 2

    def _ci_nct_lower(val_of_interest: float) -> float:
        """Internal function to compute lower confidence limit."""
        assert alpha_lower is not None  # Ensuring alpha_lower is not None
        result: float = nct.ppf(
            1 - alpha_lower, dof, val_of_interest, loc=0
        )  # Explicit type declaration
        return (result - ncp) ** 2

    def _ci_nct_upper(val_of_interest: float) -> float:
        """Internal function to compute upper confidence limit."""
        assert alpha_upper is not None  # Ensuring alpha_upper is not None
        result: float = nct.ppf(
            alpha_upper, dof, val_of_interest, loc=0
        )  # Explicit type declaration
        return (result - ncp) ** 2

    min_ncp = min(-150, -5 * ncp)
    max_ncp = max(150, 5 * ncp)

    lower_limit = minimize_scalar(
        _ci_nct_lower,
        bounds=(min_ncp, max_ncp),
        method="bounded",
        options={"xatol": tol},
    )
    upper_limit = minimize_scalar(
        _ci_nct_upper,
        bounds=(min_ncp, max_ncp),
        method="bounded",
        options={"xatol": tol, "disp": 0, "maxiter": max_iter},
    )

    return {
        "lower_limit": lower_limit.x if alpha_lower != 0 else -np.inf,
        "prob_less_lower": (
            1 - nct.cdf(ncp, dof, lower_limit.x, loc=0) if alpha_lower != 0 else 0
        ),
        "upper_limit": upper_limit.x if alpha_upper != 0 else np.inf,
        "prob_greater_upper": (
            nct.cdf(ncp, dof, upper_limit.x, loc=0) if alpha_upper != 0 else 0
        ),
    }
