import numpy as np
from data.abstract_data import Data

DEFAULT_NOISE_LEVEL = 0.2


class FrankeData(Data):
    def __init__(
        self,
        N,
        degree=1,
        random_noise=True,
        scale_data=True,
        test_size=None,
        noise_level=DEFAULT_NOISE_LEVEL,
    ):
        """The data class for the franke data

        Parameters
        ----------
            N : int
                The number of elements in the x and y directions (NOTE: total number of points is N squared)
            random_noise : bool
                Adds random noise if true
            random_positions : bool
                Sets random positions if true, else uses linspace to generate evenly spaced values
            scale_data : bool
                A bool specifying if the data should be scaled
            test_size : float/None
                Uses a specified size (0 to 1) as the test data
            noise_level : float
                The sigma value for the noise level
        """
        super().__init__()

        self.degree = degree

        data = np.random.rand(N * 2).reshape(N, 2)
        x = data[:, 0]
        y = data[:, 1]

        if random_noise:
            z = self.NoisyFrankeFunction(x, y, noise_level)
        else:
            z = self.FrankeFunction(x, y)

        if scale_data:
            z = self.scale_data(z)

        self.store_data(x, y, z, test_size)

    def store_data(self, x, y, z, test_size):
        """Stores the data, either as only x, y, and z, or splitting the x, y, and z in train/test and saving all

        Parameters
        ----------
            x : np.array
                The x data to save
            y : np.array
                The y data to save
            z : np.array
                The z data to save
            test_size : float/None
                The test size for which to store the data. None means no test data
        """
        x, y, z = np.ravel(x), np.ravel(y), np.ravel(z)

        X = self.generate_design_matrix(x, y)

        super().store_data(X, z, test_size, stratify=False)

    def get_number_of_parameters(self):
        return int((self.degree + 1) * (self.degree + 2) / 2)

    def generate_design_matrix(self, x, y):
        """Generated a design matrix given x and y values

        Parameters
        ----------
            x : np.array
                The x values for which to generate the design matrix
            y : np.array
                The y values for which to generate the design matrix

        Returns
        -------
            X : np.array
                The design matrix for the given x and y values
        """
        N = len(x)
        p = self.get_number_of_parameters()
        X = np.ones((N, p))

        for i in range(self.degree):
            q = int((i + 1) * (i + 2) / 2)
            for j in range(i + 2):
                X[:, q + j] = x ** (i - j + 1) * y ** j

        return X

    @staticmethod
    def FrankeFunction(x, y):
        """The franke function written as a numpy expression

        Parameters
        ----------
            x : np.array
                The x-values for which to generate z-values from the franke function
            y : np.array
                The y-values for which to generate z-values from the franke function

        Returns
        -------
            z : np.array
                The z values from the franke function
        """
        term1 = 0.75 * np.exp(-(0.25 * (9 * x - 2) ** 2) - 0.25 * ((9 * y - 2) ** 2))
        term2 = 0.75 * np.exp(-((9 * x + 1) ** 2) / 49.0 - 0.1 * (9 * y + 1))
        term3 = 0.5 * np.exp(-((9 * x - 7) ** 2) / 4.0 - 0.25 * ((9 * y - 3) ** 2))
        term4 = -0.2 * np.exp(-((9 * x - 4) ** 2) - (9 * y - 7) ** 2)
        return term1 + term2 + term3 + term4

    @staticmethod
    def NoisyFrankeFunction(x, y, noise_level):
        """A noisy version of the franke function

        Parameters
        ----------
            x : np.array
                The x-values for which to generate z-values from the franke function
            y : np.array
                The y-values for which to generate z-values from the franke function
            noise_level : float
                The sigma value for the amount of noise to add to the fnction

        Returns
        -------
            z : np.array
                The z values from the franke function with added noise
        """
        noise = FrankeData.generate_noise(x.shape, noise_level=noise_level)
        return FrankeData.FrankeFunction(x, y) + noise

    @staticmethod
    def generate_noise(N, noise_level=DEFAULT_NOISE_LEVEL):
        """Generates noise from a normal distribution

        Parameters
        ----------
            N : int
                The number of noises to add
            noise_level : float
                The sigma value for the amount of noise to add to the fnction

        Returns
        -------
            noise : np.array
                An array containing N values of noise with sigma noise_level
        """
        noise = np.random.normal(loc=0.0, scale=noise_level, size=N)
        return noise
