# sd: Power Spectral Decomposition Using CVXPY
Copyright (c) 2019 Bart Massey

This Python 3 code demonstrates Convex Analysis using
[CVXPY](https://www.cvxpy.org) to estimate the amplitudes of
basis spectra in a noisy measured spectrum. It was written
as a feasibility demo for an upcoming project.

The demo generates a random set of basis spectra. It then
simulates a measured spectrum comprised of the sum of random
proportions of the basis spectra and a uniform noise term.
CVXPY is used to estimate the spectral composition and noise
level of the measured spectrum. Optionally, bootstrap
confidence intervals can be computed to quantify uncertainty
in the estimates. Results are displayed textually by default,
with optional graphical display using
[`matplotlib`](https://matplotlib.org). Analysis results can
be saved as `txt` and PNG files in the current directory.

## Build and Run

Prerequisites:

* A working Python 3 installation
* `numpy`
* `cvxpy`
* `matplotlib`

It is likely that `numpy` and `matplotlib` are available in
a standard OS distro. All of the prerequisites can be
installed via `pip3 install`.

To run the program, you can just say `python3 sd.py`.

* Each run will generate a pseudo-random number generator
  seed, which can be given on the command line to repeat a
  previous run.

* You can set the noise level (default 0), the number of
  spectral samples (default 100), and the number of bases
  (default 5).

* By default, the basis prevalences (amplitudes) are
  normalized so that the largest is between 0.5 and 1.  You
  can also ask that the bases sum to exactly 1: a "complete"
  spectrum. The analysis will take this into account in its
  constraint model.

* You can set the norm used for the error computation in the
  solver. The default is to use the Linf norm: you can also
  choose the L1 norm or the always popular L2 norm.

* You can choose to use only some of the bases to form the
  spectrum, with the rest having zero prevalence. This
  "sparse" spectrum could be further optimized through
  greedy basis pursuit — see Future Work below.

* You can compute bootstrap confidence intervals with
  `--bootstrap [N]` (default 100 samples if N not specified).
  This provides uncertainty quantification for the amplitude
  estimates.

* By default, only text output is shown. Use `--show-basis`
  and/or `--show-spectrum` to display interactive plots.

* You can specify saving your analysis files to the current
  directory for later use with `--save`.

Say `python3 sd.py --help` for program usage details.

## Example

Let's try it:

    python3 sd.py --seed=27 --noise=0.2 --bootstrap

The analysis should complete quickly and print the following
text:

```
analysis (seed=27, q=0.099):
- olvium: 0.453 (0.416) [0.333, 0.507]
- afqium: 0.674 (0.674) [0.579, 0.769]
- emvium: 0.504 (0.460) [0.382, 0.556]
- ecsium: 0.158 (0.163) [0.070, 0.252]
- anpium: 0.165 (0.158) [0.081, 0.247]
- Noise: 0.200 (0.202)
- RMS error: 0.034
```

Note that the basis spectra are given randomly-generated
"element names" for convenience. The format is `true
(estimate) [CI_lower, CI_upper]`. The true values are what
the simulation used; the estimates are from the analysis.
The confidence intervals show the uncertainty in the
estimates (when `--bootstrap` is used). The `q` value is the
error in the approximation using the chosen norm (default
Linf, the maximum pointwise error): it should be small.

To view plots, add `--show-basis` and/or `--show-spectrum`:

    python3 sd.py --seed=27 --noise=0.2 --show-basis --show-spectrum

Figure 1 shows the basis spectra chosen for the analysis.

![Basis Spectra](example/basis-27.png)

Figure 2 shows the spectrum analysis: measured datapoints,
true spectrum, and estimated spectrum are displayed together,
with analysis statistics shown below the plot.

![Analysis](example/spectrum-27.png)

## Future Work

It would be useful to add a lambda parameter that
disproportionately penalized the objective function for
smaller basis amplitudes: this would likely improve the
estimates in the case where many basis components were just
not present (not a thing here).

Indeed, a parameter that outright constrained the number of
basis spectra used would be helpful for some kinds of
analysis. It is not clear how this would impact solver
performance, however: the obvious implementation would
require mixed-integer convex programming, which can be quite
expensive.

A better measurement model would be a good addition,
although at that point probably an analysis on real power
spectral data would be even better.

Greedy basis pursuit should be used to analyze "sparse"
spectra. This should give better prevalence figures in this
case.

## License

This work is made available under the "MIT License". Please
see the file `LICENSE` in this distribution for license
terms.
