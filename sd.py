#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey

# Spectral decomposition demo.

import sys

import numpy as np
import matplotlib.pyplot as plt

import spectra

# Set up seed for reproducibility.
seed=np.random.randint(1, 101)
if len(sys.argv) > 1:
    seed=int(sys.argv[1])

# Number of sample "bins" in detector.
nbins = 100
# Width of detector (usually bandwidth).
width = 100
# Number of spectra in dictionary.
ndict = 5

x = np.linspace(0, width, nbins)
sdict = spectra.sdict(ndict, 0, width)
# noise = np.random.normal(size=nbins)

fig = plt.figure(num=1, figsize=(ndict, 1.5 * ndict))
fig.subplots_adjust(hspace=1)
for s in sdict:
    fig.add_subplot(5, 1, s.id+1, title=s.name)
    plt.plot(x / width, s.spectrum(x))
fig.suptitle("Basis Spectra (seed {})".format(seed))
plt.show()
