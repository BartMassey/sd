#!/usr/bin/python3
# Copyright © 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# cvxpy spectral decomposition.

import cvxpy as cp
import numpy as np

def decompose(bases, spectrum, complete):
    """Decompose the given measured spectrum as amplitudes of
    the given bases at the sample points x.  Assume a
    uniform noise model and estimate the noise amplitude.
    If complete is true, amplitudes must sum to 1, else they
    must all be <= 1.  Return the basis amplitudes, the
    noise amplitude and the quality figure.

    """

    ndims = len(bases)

    # Create a vector of amplitude estimates.
    ampl = cp.Variable(ndims)

    # Create a noise estimate.
    noise = cp.Variable()

    # Form objective.
    obj = cp.Minimize(cp.norm(bases.T * ampl + noise - spectrum, "inf"))

    # Impose constraints.
    constraints = [
        noise >= 0, noise <= 1,
        ampl >= 0, ampl <= 1,
    ]

    if complete:
        constraints += [cp.sum(ampl) == 1]
    else:
        constraints += [ampl <= 1]

    # Form and solve problem.
    prob = cp.Problem(obj, constraints)
    prob.solve()
    assert prob.status == cp.OPTIMAL or prob.status == cp.OPTIMAL_INACCURATE
    if prob.status == cp.OPTIMAL_INACCURATE:
        print("warning: analysis reports as inaccurate")
    return (ampl.value, 0.5 * noise.value, prob.value)
