# README for Laser Calibration

This repository contains the code for calibrating a mirror for optimal ion 
response.

The main assumption made in the code here is that the ion response curve is
a Gaussian and that the peak can be approximated via a simple harmonic.

If I were to have access to experimental data and more knowledge about
data acquisition time, etc., I could perhaps implement a more physical model and
tweak the optimization.

## Overview

There are two main files: `measure.py` and `calibrate.py`. 

### measure.py

This file contains the function that effectively simulates the ion's response
by approximating a Gaussian distribution. See the function documentation in
`utils.simulate_ion_responses` for more detailed information.

### calibrate.py

This is the workhorse script. It uses the sampling from `utils` to simulate an
experiment and then implements a mesh-refinement algorithm to find the mirror
position that gives the peak response. It's more of a roll-your-own solution.

Typically, a file like this would have either a configuration file or a 
command-line interface, but for simplicity in prototyping and documentation,
I have not implemented those.

## Thoughts on the 2D-case

I used the 'extra credit' problem to explore a different solution that is 
a stochastic approach called 'basin-hopping'. 

This calibration method is a different approach as compared to the one in
the 1D case. If we wanted to just generalize that case, one approach would be
to compute an adaptive 2D mesh over the scan space (like we did in 1D) and
do another simple harmonic approximation by iteratively fitting a paraboloid.

Here, we give our mirror two degrees of freedom and attack the problem as the
optimization of a surface. We're still assuming a Gaussian distribution in
the ion's response.

This is an over-simplification as we are directly using the assumed functional
form of the response, as opposed to measurements, but it shows one potential
method of solution.
