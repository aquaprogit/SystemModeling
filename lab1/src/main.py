from generators import ExponentialGenerator
from generators import NormalGenerator
from generators import LinearCongruentialGenerator

values_count = 10000
bins = 20
test_count = 3
lambda_values = [0.1, 0.5, 15]
mean_values = [21, 10, 7]
std_dev_values = [3, 5, 5]
multiplier_values = [5 ** 13, 5 ** 6, 5 ** 12]
modulus_values = [2 ** 31, 2 ** 15, 2 ** 10]

generators = []
for lambda_param in lambda_values:
    generators.append((f'\t###__Lambda = {lambda_param}__###', ExponentialGenerator(lambda_param, values_count)))

for i in range(test_count):
    generators.append((f'\t###__Mean = {mean_values[i]}; Std Dev = {std_dev_values[i]}__###', NormalGenerator(mean_values[i], std_dev_values[i], values_count)))

for i in range(test_count):
    generators.append((f'\t###__Multiplier = {multiplier_values[i]}; Modulus = {modulus_values[i]}__###', LinearCongruentialGenerator(values_count, multiplier_values[i], modulus_values[i])))

for description, generator in generators:
    print(description)
    generator.analyze_distribution(bins)
    print()
