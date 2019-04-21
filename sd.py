#!/usr/bin/python3
# Copyright © 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Spectral decomposition demo.

import sys
import argparse

import numpy as np
import matplotlib.pyplot as plt

import spectra
import cvx

# Process arguments.
argp = argparse.ArgumentParser(
    description="Power spectral decomposition demo.")
argp.add_argument("--seed", type=int,
                  default=np.random.randint(1, 100),
                  help="PRNG seed (default randomly generated)")
argp.add_argument("--noise", type=float,
                  default=0,
                  help="noise power level (default 0)")
argp.add_argument("--bases", type=int,
                  default=5,
                  help="number of basis functions (default 5)")
argp.add_argument("--samples", type=int,
                  default=100,
                  help="spectral sample width (default 100)")
argp.add_argument("--complete", action='store_true',
                  help="require prevalences to sum to 1")
argp.add_argument("--save", action='store_true',
                  help="save analysis artifacts to files")
argp.add_argument("--hide-basis", action='store_true',
                  help="do not render the basis functions " +
                       "(true for --bases > 5)")
args = argp.parse_args()
seed = args.seed
noise = args.noise
save = args.save
nbins = args.samples
ndict = args.bases
complete = args.complete
show_basis = not args.hide_basis and ndict <= 5

# Width of detector (usually bandwidth).
width = nbins

# Set the seed.
np.random.seed(seed)

# Make basis spectra and set up sampling.
x = np.linspace(0, width, nbins)
sdict = spectra.sdict(ndict, 0, width)

# Plot basis spectra.
if show_basis:
    fig = plt.figure(num=1, figsize=(ndict, 1.5 * ndict))
    fig.subplots_adjust(hspace=1)
    for s in sdict:
        fig.add_subplot(5, 1, s.id+1, title=s.name)
        plt.plot(x, s.spectrum(x))
    fig.suptitle("Basis Spectra (seed {})".format(seed))
    if save:
        fig.savefig("basis-{}.png".format(seed))

# Normalized basis amplitude (prevalence).
ampl = np.random.random(size=ndict)
if complete:
    ampl /= np.sum(ampl)
else:
    ampl *= 0.5 * (1 + np.random.random()) / np.max(ampl)

# Implied spectrum.
bases = np.array([s.spectrum(x) for s in sdict])
spectrum = np.dot(ampl, bases) + noise

# Noisy measured spectrum.
noise_spectrum = noise * 2 * np.random.random(size=nbins)
measured = spectrum + noise_spectrum

# Print an analysis report.
def report(fout=None):
    if fout == None:
        f = sys.stdout
    else:
        f = open(fout, 'w')
    print("analysis (q={:.3f}, noise={:.3f} ({:.3f})):"
          .format(q, noise0, noise), file=f)
    for s in sdict:
        print("- {}: {:.3f} ({:.3f})"
              .format(s.name, ampl0[s.id], ampl[s.id]), file=f)
    if fout != None:
        f.close()

# Decompose measured spectrum and report
(ampl0, noise0, q) = cvx.decompose(bases, measured, complete)
report()
if save:
    report("analysis-{}.txt".format(seed))
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
if save:
    fig.savefig("spectrum-{}.png".format(seed))

# Show all plots.
plt.show()
