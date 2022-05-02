import numpy as np
from numpy.polynomial.polynomial import Polynomial

from measure import simulate_ion_responses


def main():
    # The first thing we need to do is get the "ground truth" spectrum, so
    # to speak. Since we don't have any real experimental data, we'll just
    # generate some from a Gaussian distribution with a lot of bins and a
    # lot of samples per bin to approach very closely the normal distribution.
    # In this framing of the problem, the ground truth mean (`mu_gt`) is going
    # to be the optimal mirror position.
    # For the purposes of this problem we'll assume that the optimal position
    # is between 0 and 1.
    mu_gt = 0.8
    sigma_gt = 0.05
    ground_truth_positions, ground_truth_responses = simulate_ion_responses(
        mu_gt, sigma_gt, 1000, 1000
    )

    # The idea behind this algorithm is to use a harmonic approximation to the
    # ion's response. If we have some curve that represents the ion's response
    # function, we want to identify the points that are close to the peak and
    # fit a quadratic function to those points. If we do this iteratively, we
    # should get a high-quality estimation of the optimal mirror position.
    # At each iteration, we tighten our range of points we fit the quadratic to.

    # How many iterations we should run the search and fitting algorithm for
    n_iterations = 1000
    # How many samples we should take over the interval of interest
    samples_per_iteration = 10

    # How far (as a percentage of the currently estimated optimal position) we
    # should expand our range at each iteration.
    sample_min_percent = 0.90
    sample_max_percent = 1.10

    # The minimum (maximum) indexes for the search/polynomial fitting range.
    sample_min_idx = 0
    sample_max_idx = len(ground_truth_positions)

    # The step size (as an index) to use when making measurements at a certain
    # iteration.
    sample_step = int(len(ground_truth_positions) / samples_per_iteration)
    max_coord = -1
    for iteration in range(n_iterations):
        sampled_indices = np.arange(sample_min_idx, sample_max_idx, sample_step)
        sampled_indices[-1] -= 1
        sampled_positions = ground_truth_positions[sampled_indices]
        sampled_responses = ground_truth_responses[sampled_indices]

        # If this is the first iteration, we want to center our harmonic
        # approximation near the observed maximum to deal with situations where
        # our optimal position is skewed quite off-center.
        if iteration == 0:
            max_coord = sampled_positions[np.argmax(sampled_responses)]
        else:
            # We use numpy's Polynomial.fit functionality to perform the
            # quadratic fit. Remember, we are operating under a harmonic
            # approximation near the peak of the ion response.
            fit_quadratic = Polynomial.fit(sampled_positions, sampled_responses,
                                           2)
            # These are returned as coeffs[2]x^2 + coeffs[1]x + coeffs[0]
            coeffs = fit_quadratic.convert().coef
            # Find the zero of the first derivative of the fit quadratic, i.e.,
            # the maximum.
            max_coord = - coeffs[1] / (2 * coeffs[2])

        # We want to find the index of the position closest to the maximum
        max_idx = (np.abs(ground_truth_positions - max_coord)).argmin()

        # Similarly, we want to find the indexes closest to 90% and 110% of the
        # currently estimated maximum.
        sample_min_idx = np.abs(
            ground_truth_positions
            - sample_min_percent * ground_truth_positions[max_idx]
        ).argmin()
        sample_max_idx = np.abs(
            ground_truth_positions
            - sample_max_percent * ground_truth_positions[max_idx]
        ).argmin()
        sample_step = int((sample_max_idx - sample_min_idx)
                          / samples_per_iteration)

    print(f'The estimated optimal mirror position is {max_coord}.')
    print(f'The true optimal mirror position is {mu_gt}.')
    print(f'The estimation error is {100 * (1 - (max_coord / mu_gt))}%')


if __name__ == '__main__':
    main()
