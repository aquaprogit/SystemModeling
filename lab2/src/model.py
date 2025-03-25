import numpy as np

from element import Element
from process import Process

class Model:
    def __init__(self, elements: list[Element]):
        self.elements_list = elements
        self.event = 0
        self.next_event_time = 0.0
        self.current_time = self.next_event_time

    def simulate(self, modeling_time):
        while self.current_time <= modeling_time:
            self.next_event_time = float('inf')

            for elem in self.elements_list:
                closest_time = np.min(elem.next_event_times)
                if closest_time < self.next_event_time:
                    self.next_event_time = closest_time
                    self.event = elem.id

            for elem in self.elements_list:
                elem.calculate(self.next_event_time - self.current_time)

            self.current_time = self.next_event_time

            for elem in self.elements_list:
                elem.current_time = self.current_time

            if len(self.elements_list) > self.event:
                self.elements_list[self.event].out_act()

            for elem in self.elements_list:
                if self.current_time in elem.next_event_times:
                    elem.out_act()

            self.print_info()

        return self.print_result()

    def print_info(self):
        for e in self.elements_list:
            e.print_info()

    def print_result(self):
        print('-----RESULT-----')

        global_max_observed_queue_length = 0
        global_mean_queue_length_accumulator = 0
        global_failure_probability_accumulator = 0
        global_mean_load_accumulator = 0
        num_of_processors = 0

        for elem in self.elements_list:
            elem.result()
            if isinstance(elem, Process):
                num_of_processors += 1
                mean_queue_length = elem.mean_queue / self.current_time

                failure_probability = elem.failure_count / (elem.quantity + elem.failure_count) if (elem.quantity + elem.failure_count) != 0 else 0

                mean_load = elem.mean_load / self.current_time

                global_mean_queue_length_accumulator += mean_queue_length
                global_failure_probability_accumulator += failure_probability
                global_mean_load_accumulator += mean_load

                if elem.max_observed_queue > global_max_observed_queue_length:
                    global_max_observed_queue_length = elem.max_observed_queue

                print(f"Average queue length: {mean_queue_length}")
                print(f"Failure probability: {failure_probability}")
                print(f"Average load: {mean_load}")
                print()

        global_mean_queue_length = global_mean_queue_length_accumulator / num_of_processors
        global_failure_probability = global_failure_probability_accumulator / num_of_processors
        global_mean_load = global_mean_load_accumulator / num_of_processors

        print(f"Global max observed queue length: {global_max_observed_queue_length}")
        print(f"Global mean queue length: {global_mean_queue_length}")
        print(f"Global failure probability: {global_failure_probability}")
        print(f"Global mean load: {global_mean_load}")
        print()

        return {
            "global_max_observed_queue_length": global_max_observed_queue_length,
            "global_mean_queue_length": global_mean_queue_length,
            "global_failure_probability": global_failure_probability,
            "global_mean_load": global_mean_load
        }
