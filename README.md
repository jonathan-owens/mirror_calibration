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
