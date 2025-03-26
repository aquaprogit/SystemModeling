import fun_rand as fun
from copy import deepcopy
import numpy as np


class Element:
    nextId = 0

    def __init__(self, name=None, delay_mean=1., delay_dev=0., distribution='', probability=1, channels_count=1,
                 max_queue=float('inf')):
        self.next_times = [0] * channels_count
        self.delay_mean = delay_mean
        self.delay_dev = delay_dev
        self.quantity = 0
        self.current_time = 0
        self.states = [0] * channels_count
        self.next_element = None
        self.element_id = Element.nextId
        Element.nextId += 1
        self.name = f'Element_{self.element_id}' if name is None else name
        self.distribution = distribution
        self.probabilities = [probability]
        self.priorities = [1]
        self.queue_len = 0
        self.max_observed_queue_len = 0
        self.max_queue_len = max_queue
        self.mean_queue_len = 0.0
        self.channels_count = channels_count
        self.mean_load = 0
        self.failure_quantity = 0

    def choose_next_element(self):
        if self.probabilities != [1] and self.priorities != [1]:
            raise Exception('Route selection is ambiguous: probability and priority are set simultaneously')
        elif self.probabilities != [1]:
            next_element = np.random.choice(a=self.next_element, p=self.probabilities)
            return next_element
        elif self.priorities != [1]:
            next_element = self.choose_by_priority()
            return next_element
        elif self.probabilities == [1] and self.priorities == [1]:
            return self.next_element[0]

    def choose_by_priority(self):
        priorities = deepcopy(self.priorities)
        min_queue = float('inf')
        min_queue_index = 0

        for p in range(len(priorities)):
            if min(priorities) == 100000:
                break

            max_pr_index = priorities.index(min(priorities))
            if 0 in self.next_element[max_pr_index].states:
                return self.next_element[max_pr_index]
            else:
                if self.next_element[max_pr_index].queue_len < min_queue:
                    min_queue = self.next_element[max_pr_index].queue_len
                    min_queue_index = self.next_element.index(self.next_element[max_pr_index])

            priorities[max_pr_index] = 100000

        return self.next_element[min_queue_index]

    def get_delay(self):
        if 'exp' == self.distribution:
            return fun.exp(self.delay_mean)
        elif 'norm' == self.distribution:
            return fun.norm(self.delay_mean, self.delay_dev)
        elif 'uniform' == self.distribution:
            return fun.uniform(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean

    def enter(self):
        pass

    def get_state(self):
        return self.states

    def set_state(self, new_state):
        self.states = new_state

    def set_t_next(self, t_next_new):
        self.next_times = t_next_new

    def get_t_curr(self):
        return self.current_time

    def leave(self):
        self.quantity += 1

    def result(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.states}')

    def print_info(self):
        print(f'{self.name} state = {self.states} quantity = {self.quantity} t_next = {self.next_times}')

    def get_free_channels(self):
        free_channels = []
        for i in range(self.channels_count):
            if self.states[i] == 0:
                free_channels.append(i)

        return free_channels

    def get_current_channels(self):
        current_channels = []
        for i in range(self.channels_count):
            if self.next_times[i] == self.current_time:
                current_channels.append(i)
        return current_channels
