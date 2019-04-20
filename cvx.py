#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey

# cvxpy spectral decomposition.

import cvxpy as cp
import numpy as np

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
