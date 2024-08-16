"""Noncentral t-distribution module."""

# --------------------------- Import libraries and functions --------------------------
from typing import Any, Dict, Optional, Union

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import nct

from pycvcqv.checkers import is_dof_positive_natural_number, is_ncp_huge
from pycvcqv.sanitizers import validate_ncp_confidence_level_arguments

# -------------------------------- function definition --------------------------------


def _ci_nct_lower(
    val_of_interest: float, alpha_lower: float, dof: int, ncp: float
) -> float:
    """Computes lower confidence limit for noncentral t parameter."""
    # ------------------------ Ensuring alpha_lower is not None -----------------------
    result: float = nct.ppf(1 - alpha_lower, dof, val_of_interest, loc=0)
    return (result - ncp) ** 2


def _ci_nct_upper(
    val_of_interest: float, alpha_upper: float, dof: int, ncp: float
) -> float:
    """Computes upper confidence limit for noncentral t parameter."""
    # ------------------------ Ensuring alpha_lower is not None -----------------------
    result: float = nct.ppf(alpha_upper, dof, val_of_interest, loc=0)
    return (result - ncp) ** 2


def _calculate_alpha_tails(
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
) -> Dict[str, Any]:
    """Calculates alpha tails of noncentral t parameter confidence interval."""
    # ----- If all three are None, use default conf_level and compute alpha values ----
    if all(scalar is None for scalar in [conf_level, alpha_lower, alpha_upper]):
        conf_level = 0.95
        alpha_lower = alpha_upper = (1 - conf_level) / 2
    # ------ Calculate the alpha_lower and alpha_upper based on given conf_level ------
    elif conf_level is not None and all(
        scalar is None for scalar in [alpha_lower, alpha_upper]
    ):
        alpha_lower = alpha_upper = (1 - conf_level) / 2
    # ------------------------ Preparing the alpha tails output -----------------------
    alpha_tails = {"alpha_lower": alpha_lower, "alpha_upper": alpha_upper}
    return alpha_tails


def _calculate_out_of_range_probabilities(
    ncp: float,
    dof: int,
    ncp_lower_limit: float,
    valid_alpha_lower: float,
    ncp_upper_limit: float,
    valid_alpha_upper: float,
) -> Dict[str, Any]:
    """
    Calculates the probabilities for out of range of noncentral t parameter
    confidence interval.
    """
    # ------------- Probability that the NCP is less than the lower limit -------------
    prob_less_lower = (
        1 - nct.cdf(ncp, dof, ncp_lower_limit, loc=0) if valid_alpha_lower != 0 else 0
    )
    # ------------ Probability that the NCP is greater than the upper limit -----------
    prob_greater_upper = (
        nct.cdf(ncp, dof, ncp_upper_limit, loc=0) if valid_alpha_upper != 0 else 0
    )
    # -------------------- Preparing the out of range probabilities -------------------
    out_of_range_probabilities = {
        "prob_less_lower": prob_less_lower,
        "prob_greater_upper": prob_greater_upper,
    }
    return out_of_range_probabilities


# ------------------ Decorators to check validity of input arguments ------------------
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
    # ------ Calculates alpha tails of noncentral t parameter confidence interval -----
    alpha_tails = _calculate_alpha_tails(conf_level, alpha_lower, alpha_upper)
    valid_alpha_lower = alpha_tails["alpha_lower"]
    valid_alpha_upper = alpha_tails["alpha_upper"]
    # ------------------------ allowed minimum and maximum NCP ------------------------
    min_ncp = min(-150, -5 * ncp)
    max_ncp = max(150, 5 * ncp)
    # ------------------------- calculate lower_limit for NCP -------------------------
    ncp_lower_limit = minimize_scalar(
        _ci_nct_lower,
        bounds=(min_ncp, max_ncp),
        method="bounded",
        options={"xatol": tol, "disp": 0, "maxiter": max_iter},
        args=(valid_alpha_lower, dof, ncp),
    ).x
    # ------------------------- calculate upper_limit for NCP -------------------------
    ncp_upper_limit = minimize_scalar(
        _ci_nct_upper,
        bounds=(min_ncp, max_ncp),
        method="bounded",
        options={"xatol": tol, "disp": 0, "maxiter": max_iter},
        args=(valid_alpha_upper, dof, ncp),
    ).x
    # -------------- Calculates the probabilities for out of range values -------------
    out_of_range_probabilities = _calculate_out_of_range_probabilities(
        ncp,
        dof,
        ncp_lower_limit,
        valid_alpha_lower,
        ncp_upper_limit,
        valid_alpha_upper,
    )
    # ----------------------------- preparing the result  -----------------------------
    result = {
        "lower_limit": ncp_lower_limit if valid_alpha_lower != 0 else -np.inf,
        "prob_less_lower": out_of_range_probabilities["prob_less_lower"],
        "upper_limit": ncp_upper_limit if valid_alpha_upper != 0 else np.inf,
        "prob_greater_upper": out_of_range_probabilities["prob_greater_upper"],
    }
    return result


# ------------------ Decorators to check validity of input arguments ------------------
@is_dof_positive_natural_number
@is_ncp_huge
@validate_ncp_confidence_level_arguments
def conf_limits_nct_minimize(
    ncp: float,
    dof: int,
    conf_level: Optional[float] = None,
    alpha_lower: Optional[float] = None,
    alpha_upper: Optional[float] = None,
    tol: Optional[float] = 1e-9,
) -> Dict[str, Union[float, int]]:
    """
    Calculate confidence limits for the noncentrality parameter (NCP) of the
    noncentral t-distribution using scipy.optimize.minimize.

    This function uses the scipy.optimize.minimize method to estimate
    the lower and upper confidence limits for the noncentrality
    parameter (NCP) given the degrees of freedom, confidence level, and other parameters.

    Args:
        ncp (float): The observed noncentrality parameter. Can be passed as 't_value'.
        dof (int): Degrees of freedom. Must be positive.
        conf_level (float, optional): The confidence level for the interval.
        alpha_lower (float, optional): The significance level for the lower tail.
        alpha_upper (float, optional): The significance level for the upper tail.
        tol (float, optional): Tolerance for the optimization algorithms. Default is 1e-9.

    Returns:
        dict: A dictionary with the following keys:
            - lower_limit (float): Lower confidence limit for the NCP.
            - prob_less_lower (float): Probability that the NCP is less than the lower limit.
            - upper_limit (float): Upper confidence limit for the NCP.
            - prob_greater_upper (float): Probability that the NCP is greater than the upper limit.

    Example:
        .. code:: python
            >>> conf_limits_nct_minimize(ncp=2.83, dof=126, conf_level=0.95)
            ...     {
            ...     'lower_limit': 0.833750253390236,
            ...     'prob_less_lower': 0.024999999571209908,
            ...     'upper_limit': 4.815359132565956,
            ...     'prob_greater_upper': 0.025000000428616057
            ...     }
    """
    # ------ Calculates alpha tails of noncentral t parameter confidence interval -----
    alpha_tails = _calculate_alpha_tails(conf_level, alpha_lower, alpha_upper)
    valid_alpha_lower = alpha_tails["alpha_lower"]
    valid_alpha_upper = alpha_tails["alpha_upper"]
    # ------------------------- calculate lower_limit for NCP -------------------------
    ncp_lower_limit = minimize(
        _ci_nct_lower, ncp, tol=tol, args=(valid_alpha_upper, dof, ncp)
    ).x[0]
    # ------------------------- calculate upper_limit for NCP -------------------------
    ncp_upper_limit = minimize(
        _ci_nct_upper, ncp, tol=tol, args=(valid_alpha_upper, dof, ncp)
    ).x[0]
    # -------------- Calculates the probabilities for out of range values -------------
    out_of_range_probabilities = _calculate_out_of_range_probabilities(
        ncp,
        dof,
        ncp_lower_limit,
        valid_alpha_lower,
        ncp_upper_limit,
        valid_alpha_upper,
    )
    # ----------------------------- preparing the result  -----------------------------
    result = {
        "lower_limit": ncp_lower_limit if valid_alpha_lower != 0 else -np.inf,
        "prob_less_lower": out_of_range_probabilities["prob_less_lower"],
        "upper_limit": ncp_upper_limit if valid_alpha_upper != 0 else np.inf,
        "prob_greater_upper": out_of_range_probabilities["prob_greater_upper"],
    }
    return result
