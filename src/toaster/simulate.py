"""Symbolic binding and parameter sweeps. WP-5 implements sweep_1d fully."""

import numpy as np
from typing import Callable


def sweep_1d(fn: Callable, axis: np.ndarray, **fixed) -> np.ndarray:
    """Evaluate fn over a 1-D parameter grid with all other parameters fixed.

    fn is a lambdified sympy expression.
    axis is the values for the swept parameter (first positional arg of fn).
    fixed keyword args are passed as remaining positional args in definition order.
    """
    return fn(axis, **fixed)
