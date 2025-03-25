import numpy as np
import random
import utils

class BaseGenerator:
    def __init__(self, sample_size):
        self.sample_size = sample_size
        self.data = self.generate_data()

    def generate_data(self):
        return np.array([])

    def compute_expected_value(self, intervals, index):
        pass

    def get_expected_values(self, histogram_data, num_intervals):
        expected_values = []
        interval_bounds = utils.extract_interval_bounds(histogram_data, num_intervals)

        for index in range(num_intervals):
            expected_values.append(self.compute_expected_value(interval_bounds, index))

        return expected_values

    def analyze_distribution(self, num_intervals):
        mean_value, variance = utils.compute_mean_and_variance(self.data)
        histogram_data = utils.compute_intervals(self.data, num_intervals)
        utils.plot_distribution_histogram(histogram_data, num_intervals)
        
        expected_values = self.get_expected_values(histogram_data, num_intervals)
        observed_values = [entry[1] for entry in histogram_data]
        chi_square_statistic = utils.compute_chi_squared(expected_values, observed_values, num_intervals)

        utils.display_statistics(mean_value, variance, chi_square_statistic)

class ExponentialGenerator(BaseGenerator):
    def __init__(self, lambda_param, sample_size):
        self.lambda_param = lambda_param
        super().__init__(sample_size)

    def generate_data(self):
        return np.array([-np.log(random.random()) / self.lambda_param for _ in range(self.sample_size)])

    def compute_expected_value(self, intervals, index):
        return utils.exponential_distribution_probability(intervals[index][0], intervals[index][1], self.lambda_param)

def generate_gaussian_offset():
    return sum(random.random() for _ in range(12)) - 6

class NormalGenerator(BaseGenerator):
    def __init__(self, mean, std_dev, sample_size):
        self.mean = mean
        self.std_dev = std_dev
        super().__init__(sample_size)

    def generate_data(self):
        return np.array([self.std_dev * generate_gaussian_offset() + self.mean for _ in range(self.sample_size)])

    def compute_expected_value(self, intervals, index):
        return utils.normal_distribution_probability(intervals[index][0], intervals[index][1], self.mean, self.std_dev)

class LinearCongruentialGenerator(BaseGenerator):
    def __init__(self, sample_size, multiplier, modulus):
        self.multiplier = multiplier
        self.modulus = modulus
        super().__init__(sample_size)

    def generate_data(self):
        seed_value = self.multiplier * random.random() % self.modulus
        data_samples = np.array([])

        for _ in range(self.sample_size):
            seed_value = self.multiplier * seed_value % self.modulus
            data_samples = np.append(data_samples, seed_value / self.modulus)

        return data_samples

    def compute_expected_value(self, intervals, index):
        return (intervals[index][1] - intervals[index][0]) / (max(self.data) - min(self.data))
