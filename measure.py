import numpy as np
import matplotlib.pyplot as plt


def simulate_ion_responses(mu, sigma, n_samples_per_bin=100, n_bins=100):
    """
    This function simulates the ion responses by generating a normal
    distribution centered at `mu` with a spread of `sigma`. Each bin is
    effectively the position of the mirror and the `n_samples_per_bin` is the
    number of pulses to fire with a laser at that position. The quality metric
    is then the number of counts per bin.

    The idea is that the physical nature of response is going to peak at some
    position (effectively `mu`). If we sample from a normal distribution with
    a reasonably large number of samples we will get an approximate
    representation of a normal distribution.

    :param mu: The position of the peak ion response
    :type mu: float

    :param sigma: The standard deviation of the normal distribution simulating
    the response curve
    :type sigma: float

    :param n_samples_per_bin: How many samples per bin in the histogram.
    :type n_samples_per_bin: int

    :param n_bins: How many bins in the histogram
    :type n_bins: int

    :return: the mirror positions and their corresponding ion responses
    :rtype: [float], [float]
    """
    samples = np.random.normal(mu, sigma, n_samples_per_bin * n_bins)
    # samples = np.random.poisson(mu, n_bins)
    # We truncate the range of the sampled data from [0, 1] in order to more
    # represent the physical reality that the peak would likely not be centered
    # in the position range.
    response, position, _ = plt.hist(samples, n_bins, range=[0, 1],
                                     density=True)

    # plt.hist actually returns and array of length n_bins+1 in position
    # where each element (except the last) is the left edge of the bin. The
    # final element is the right edge of the bin. We do a quick conversion here
    # so that we are returning the mid-points of the bins.
    midpoints = np.zeros(n_bins)
    for bin_n in range(n_bins):
        midpoints[bin_n] = (position[bin_n + 1] - position[bin_n]) \
                           / 2 + position[bin_n]
    position = midpoints

    return position, response
