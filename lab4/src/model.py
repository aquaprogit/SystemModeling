import numpy as np

from element import Element


class Model:
    def __init__(self, elements: list[Element]):
        self.list = elements
        self.element_id = 0
        self.next_time = 0.0
        self.current_time = self.next_time

    def simulate(self, time):
        while self.current_time < time:
            self.next_time = float('inf')

            for e in self.list:
                t_next_val = np.min(e.next_times)
                if t_next_val < self.next_time:
                    self.next_time = t_next_val
                    self.element_id = e.element_id

            self.current_time = self.next_time

            for e in self.list:
                e.current_time = self.current_time

            if len(self.list) > self.element_id:
                self.list[self.element_id].leave()

            for e in self.list:
                if self.current_time in e.next_times:
                    e.leave()
