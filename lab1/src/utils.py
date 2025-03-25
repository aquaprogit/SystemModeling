import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import integrate

def print_generator_name(generator_number):
    print(f'\t###__GENERATOR #{generator_number}__###')

def display_statistics(mean, variance, chi_squared_value):
    print(f'\nChi squared: {chi_squared_value}')
    print(f'Average: {mean}')
    print(f'Dispersion: {variance}')

def compute_mean_and_variance(data_array):
    mean_value = data_array.mean()
    variance = np.var(data_array, ddof=1)
    return mean_value, variance

def compute_intervals(data_array, num_intervals):
    interval_width = (data_array.max() - data_array.min()) / num_intervals
    intervals = []
    lower_bound = data_array.min()

    for _ in range(num_intervals):
        upper_bound = lower_bound + interval_width
        count = np.sum((data_array >= lower_bound) & (data_array < upper_bound))
        intervals.append([[lower_bound, upper_bound], count])
        lower_bound = upper_bound
    
    return intervals

def extract_interval_bounds(interval_data, num_intervals):
    return [[interval_data[i][0][0], interval_data[i][0][1]] for i in range(num_intervals)]

def convert_to_dataframe(interval_data, num_intervals):
    interval_labels = [f'{round(interval[0][0], 2)}-{round(interval[0][1], 2)}' for interval in interval_data]
    values = [interval[1] for interval in interval_data]
    return pd.DataFrame({'Intervals': interval_labels, 'Values': values})

def plot_distribution_histogram(interval_data, num_intervals):
    df = convert_to_dataframe(interval_data, num_intervals)
    print(df.head(num_intervals))
    sns.barplot(data=df, x='Intervals', y='Values', color='g', edgecolor='black')
    plt.tight_layout()
    plt.xticks(rotation=29)
    plt.show()

def compute_chi_squared(expected_values, observed_values, num_intervals):
    chi_squared = sum((observed_values[i] - (10000 * expected_values[i]))**2 / (10000 * expected_values[i]) for i in range(num_intervals))
    return chi_squared

def exponential_distribution_probability(lower_bound, upper_bound, lambda_param):
    return np.exp(-lambda_param * lower_bound) - np.exp(-lambda_param * upper_bound)

def normal_distribution_probability(lower_bound, upper_bound, mean, std_dev):
    pdf_function = lambda x: (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-((x - mean) ** 2) / (2 * std_dev ** 2))
    probability, _ = integrate.quad(pdf_function, lower_bound, upper_bound)
    return probability
