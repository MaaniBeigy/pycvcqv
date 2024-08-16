"""The checkers traits."""

# --------------------------- Import libraries and functions --------------------------
# -------------------------------- function definition --------------------------------


def validate_ncp_confidence_level_arguments(function):
    """Decorator to validate noncentrality parameter confidence interval arguments."""

    def wrapper(*args, **kwargs):
        """The wrapper function."""
        # ------------ Validate that conf_level is in the range [0, 1] ------------
        # ---------------- Extract the positional or keyword arguments ----------------
        conf_level = kwargs.get("conf_level", args[2] if len(args) > 2 else None)
        alpha_lower = kwargs.get("alpha_lower", args[3] if len(args) > 3 else None)
        alpha_upper = kwargs.get("alpha_upper", args[4] if len(args) > 4 else None)

        # -- Validate if one of alpha_lower or alpha_upper is given, both must be given
        if (alpha_lower is not None) != (alpha_upper is not None):
            raise ValueError(
                "Both alpha_lower and alpha_upper must be provided or both None."
            )

        # --- Validate that alpha_lower and alpha_upper are within the [0, 1] range ---
        if alpha_lower is not None:
            if not 0 <= alpha_lower <= 1:
                raise ValueError(
                    "conf_level and alpha values must be in the range [0, 1]."
                )
        if alpha_upper is not None:
            if not 0 <= alpha_upper <= 1:
                raise ValueError(
                    "conf_level and alpha values must be in the range [0, 1]."
                )
        if conf_level is not None:
            if not 0 <= conf_level <= 1:
                raise ValueError(
                    "conf_level and alpha values must be in the range [0, 1]."
                )
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
