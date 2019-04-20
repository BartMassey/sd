#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey

# Spectral decomposition demo.

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

def ugauss(x, loc=0, scale=1, *args, **kwargs):
    "Gaussian with unit amplitude, center loc, deviation scale."
    xm = (x - loc) / scale
    return np.exp(-(xm * xm) / 2, *args, **kwargs)

def gauss(x, loc=0, scale=1, *args, **kwargs):
    "Gaussian with unit area, center loc, deviation scale."
    norm = scale * np.sqrt(2.0 * np.pi)
    return ugauss(x, loc, scale, *args, **kwargs) / norm

def spectrum(low, high, *args, **kwargs):
    """A "random spectrum" of superposed Gaussian peaks. The
    center of each peak is placed in the range
    [low..high]. Peak amplitudes are always less than 1.0,
    but the overall spectrum can be higher.
    """
    # 2-5 peaks.
    npeaks = 2 + np.random.randint(0, 4)

    # Generate peaks.
    peaks = list()
    # XXX There's probably a cleaner way to do this by
    # broadcasting random numbers. Meh.
    for _ in range(npeaks + 1):
        # Uniform random location in [high..low].
        loc = (high - low) * np.random.rand() + low
        # Uniform random height in [0.1..1).
        height = 0.1 + 0.9 * np.random.rand()
        # XXX "Plausible" random scale.
        scale = (high - low) * (0.025 + 0.125 * np.random.rand())
        peaks.append((loc, height, scale))

    # The spectrum function we will return.
    norm = 1
    def sf(x, *args, **kwargs):
        p = [height * ugauss(x, loc, scale) for loc, height, scale in peaks]
        return sum(p)

    return sf

x = np.linspace(0, 100, 1000)
s = spectrum(0, 100)
plt.plot(x, s(x))
plt.show()

exit(0)

# Create a scalar optimization vector.
cx = [-0.2,-2.1,0.1,5.4]
cy = np.array(list(map(gauss, cx)))
print(cy)
cz = cy + np.random.rand(4)
print(cz)

x = cp.Variable()

# Create two constraints.
constraints = [x * cy <= cz]

# Form objective.
obj = cp.Minimize(cp.norm(cz - x*cy,1))

# Form and solve problem.
prob = cp.Problem(obj, constraints)
prob.solve()  # Returns the optimal value.
print("status:", prob.status)
print("optimal value", prob.value)
print("optimal var", x.value)
