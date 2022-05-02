import numpy as np


class Measure2D:
    def __init__(self, mu_x, mu_y, sigma_x, sigma_y, amplitude):
        """
        This measurement class is meant to simulate the act of taking an ion
        response measurement at some location on a 2D grid.

        :param mu_x: The x-location of the center of the Gaussian
        :type mu_x: float

        :param mu_y: The y-location of the center of the Gaussian
        :type mu_y: float

        :param sigma_x: The x-sigma in the Gaussian
        :type sigma_x: float

        :param sigma_y: The y-sigma in the Gaussian
        :type sigma_y: float

        :param amplitude: The amplitude of the 2D Gaussian
        :type amplitude: float
        """
        self.mu_x = mu_x
        self.mu_y = mu_y
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        self.amplitude = amplitude

    def measure(self, x):
        """
        Return a 'measurement' at the coordinate x = (x, y) based on the
        Gaussian distribution:

        -1 * self.amplitude * np.exp(-1 * (
                (x[0] - self.mu_x)**2 / (2 * self.sigma_x**2)
                + (x[1] - self.mu_y)**2 / (2 * self.sigma_y**2)
        ))

        Note here that we multiply by -1 because we are using a minimization
        function, so we want to turn our maximum into a minimum.

        :param x: The coordinate at which to take a measurement, where x[0] = x
        and x[1] = y.
        :type x: [float, float]

        :return: The value of the Gaussian at `x`
        :rtype: float
        """
        return -1 * self.amplitude * np.exp(-1 * (
                (x[0] - self.mu_x)**2 / (2 * self.sigma_x**2)
                + (x[1] - self.mu_y)**2 / (2 * self.sigma_y**2)
        ))
