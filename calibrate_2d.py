import numpy as np
from scipy.optimize import basinhopping

from measure_2d import Measure2D


"""
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
"""


def main():
    amplitude = 1.0
    # x_0 and y_0 are the ground truth peak for selecting the optimal mirror
    # position
    x_0 = 0.4
    y_0 = 0.6
    sigma_x = 0.05
    sigma_y = 0.05

    n_iterations = 100

    gauss_2d = Measure2D(x_0, y_0, sigma_x, sigma_y, amplitude)

    minimizer_kwargs = {"method": "L-BFGS-B"}
    initial_guess = [0.2, 0.8]

    # We use the stochastic basin-hopping algorithm here as one approach.
    ret = basinhopping(gauss_2d.measure, initial_guess,
                       minimizer_kwargs=minimizer_kwargs, niter=n_iterations)

    x_opt, y_opt = ret.x
    print(f'The estimated optimal mirror position is ({x_opt}, {y_opt}).')
    print(f'The true optimal mirror position is ({x_0}, {y_0}).')
    print(f'The estimation error is ({np.abs(x_opt - x_0)}, {np.abs(y_opt - y_0)})')


if __name__ == '__main__':
    main()
