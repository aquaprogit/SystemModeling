import numpy as np

from bank.process_bank import ProcessBank
from hospital.process_hospital import ProcessHospital
from universal.process import Process


class Model:
    def __init__(self, elements: list):
        self.list = elements
        self.event = 0
        self.t_next = 0.0
        self.t_curr = self.t_next

    # здійснення імітації на інтервалі часу time
    def simulate(self, time):
        while self.t_curr < time:
            # встановити t_next на max value of float
            self.t_next = float('inf')

            for e in self.list:
                # знаходимо найменший з моментів часу
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = e.id_el

            for e in self.list:
                e.calculate(self.t_next - self.t_curr)

            # просунутися у часі вперед
            self.t_curr = self.t_next

            # оновити поточний час для кожного елементу
            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()

            self.print_info()
        self.print_result()

    def print_info(self):
        for e in self.list:
            e.print_info()

    def print_result(self):
        print('-----RESULT-----')

        global_max_observed_queue_length = 0
        global_mean_queue_length_accumulator = 0
        global_failure_probability_accumulator = 0
        global_mean_load_accumulator = 0
        num_of_processors = 0

        for e in self.list:
            e.result()
            if isinstance(e, Process) or isinstance(e, ProcessBank) or isinstance(e, ProcessHospital):
                num_of_processors += 1
                mean_queue_length = e.mean_queue / self.t_curr

                failure_probability = e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0

                # розрахунок середнього завантаження пристрою
                mean_load = e.mean_load / self.t_curr

                global_mean_queue_length_accumulator += mean_queue_length
                global_failure_probability_accumulator += failure_probability
                global_mean_load_accumulator += mean_load

                if e.max_observed_queue > global_max_observed_queue_length:
                    global_max_observed_queue_length = e.max_observed_queue

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
