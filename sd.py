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

# Make basis spectra and set up sampling.
x = np.linspace(0, width, nbins)
sdict = spectra.sdict(ndict, 0, width)

# Plot basis spectra.
fig = plt.figure(num=1, figsize=(ndict, 1.5 * ndict))
fig.subplots_adjust(hspace=1)
for s in sdict:
    fig.add_subplot(5, 1, s.id+1, title=s.name)
    plt.plot(x, s.spectrum(x))
fig.suptitle("Basis Spectra (seed {})".format(seed))

# Basis amplitude (prevalence).
ampl = np.random.random(size=ndict)

# Implied spectrum.
bases = np.array([s.spectrum(x) for s in sdict])
spectrum = np.dot(ampl, bases)

# Noisy measured spectrum.
noise = 0.2 * np.random.random(size=nbins)
measured = spectrum + noise

# Plot starting points.
fig = plt.figure(num=2, figsize=(5, 5))
fig.subplots_adjust(hspace=0.5)
fig.add_subplot(2, 1, 1, title="implied")
plt.plot(x, spectrum)
fig.add_subplot(2, 1, 2, title="measured")
plt.plot(x, measured)
fig.suptitle("Spectrum")

# Show all plots.
plt.show()
