#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey

# cvxpy spectral decomposition.

import cvxpy as cp
import numpy as np

def decompose(bases, spectrum):
    """Decompose the given measured spectrum as amplitudes of
    the given bases at the sample points x.  Assume a
    uniform noise model and estimate the noise amplitude.
    Return the basis amplitudes and the noise amplitude.

    """

    # Create a vector of amplitude estimates.
    ampl = cp.Variable(len(bases))

    # Create a noise estimate.
    noise = cp.Variable()

    # Form objective.
    obj = cp.Minimize(cp.norm(bases.T * ampl + noise - spectrum, 2))

    # Add some sanity constraints.
    constraints = [noise <= 1, ampl <= len(bases)]

    # Form and solve problem.
    prob = cp.Problem(obj, constraints)
    prob.solve()
    assert prob.status == cp.OPTIMAL or prob.status == cp.OPTIMAL_INACCURATE
    if prob.status == cp.OPTIMAL_INACCURATE:
        print("warning: analysis reports as inaccurate")
    return (ampl.value, noise.value, prob.value)
