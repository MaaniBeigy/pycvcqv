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
