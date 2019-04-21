#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey

# Spectral decomposition demo.

import sys

import numpy as np
import matplotlib.pyplot as plt

import spectra
import cvx

# Set up seed for reproducibility.
if len(sys.argv) > 1:
    seed=int(sys.argv[1])
else:
    seed=np.random.randint(1, 101)
np.random.seed(seed)

# Number of sample "bins" in detector.
nbins = 100
# Width of detector (usually bandwidth).
width = 100
# Number of spectra in dictionary.
ndict = 5
# Mean noise level for measurement.
noise = 0.2

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
spectrum = np.dot(ampl, bases) + noise

# Noisy measured spectrum.
noise_spectrum = noise * 2 * np.random.random(size=nbins)
measured = spectrum + noise_spectrum

# Decompose measured spectrum and report
(ampl0, noise0, q) = cvx.decompose(bases, measured)
print("analysis (q={:.3f}, noise={:.3f} ({:.3f})):".format(q, noise0, noise))
for s in sdict:
    print("- {}: {:.3f} ({:.3f})".format(s.name, ampl0[s.id], ampl[s.id]))
print()
spectrum0 = np.dot(ampl0, bases) + noise0

# Plot analysis.
fig = plt.figure(num=2, figsize=(6, 5))
fig.subplots_adjust(hspace=1)
fig.add_subplot(2, 1, 1, title="measured")
plt.plot(x, measured, 'o', markersize=2)
fig.add_subplot(2, 1, 2, title="analyzed")
label = "true (noise {:.3f})".format(noise)
plt.plot(x, spectrum, label=label)
label = "est (noise {:.3f})".format(noise0)
plt.plot(x, spectrum0, label=label)
plt.legend()
fig.suptitle("Spectrum")

# Show all plots.
plt.show()
