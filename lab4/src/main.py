import time
from element import Element
from model import Model
import model_builders as mb
import matplotlib.pyplot as plt


def analyze_theoretical(model: Model, modeling_time: int):
    base_value = 0

    for elem in model.list:
        base_value += (1 / elem.delay_mean) if elem.delay_mean != 0 else 0

    base_value = base_value / len(model.list)

    count_accum = 0
    for i in range(len(model.list) - 1):
        if model.list[i].next_element is None or not len(model.list[i].next_element) >= 2:
            count_accum += 1
    return (base_value * count_accum) * modeling_time * 3


def analyze(model_builder: mb.ModelBuilder):
    modeling_time = 1000
    time_to_test = 3
    elems_to_test = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    analytic_time = []
    theoretical_operation_count = []
    for i in elems_to_test:
        print(f'Testing with {i} elems')
        analytic_time_accumulator = 0
        theoretical_operation_count_accumulator = 0
        for j in range(time_to_test):
            c1, model = model_builder.build(i)
            theoretical_operation_count_accumulator += analyze_theoretical(model, modeling_time)
            start_time = time.perf_counter()
            model.simulate(modeling_time)
            end_time = time.perf_counter()
            analytic_time_accumulator += end_time - start_time
        analytic_time.append(analytic_time_accumulator / time_to_test)
        theoretical_operation_count.append(theoretical_operation_count_accumulator / time_to_test)

    plt.title("Analytic estimation")
    plt.xlabel("Model complexity")
    plt.ylabel("Time")
    plt.plot(elems_to_test, analytic_time, color="green")
    plt.show()

    plt.title("Theoretical estimation")
    plt.xlabel("Model complexity")
    plt.ylabel("Operations")
    plt.plot(elems_to_test, theoretical_operation_count, color="green")
    plt.show()


def main():
    print("Starting to analyze simple model")
    analyze(mb.SimpleModelBuilder())
    input("Finished simple model. Press enter to analyze complex model")
    analyze(mb.ComplexModelBuilder())
    print("Finished complex model.")


if __name__ == "__main__":
    main()
