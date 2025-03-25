import numpy as np
import element as e


class Process(e.Element):
    def __init__(self, delay, channels=1):
        super().__init__(delay)
        self.queue = 0
        self.max_observed_queue = 0
        self.max_queue = float('inf')
        self.mean_queue = 0.0
        self.failure_count = 0
        self.mean_load = 0
        self.channels_count = channels
        self.next_event_times = [np.inf]*self.channels_count
        self.states = [0]*self.channels_count
        self.probability = [1]

    def in_act(self):
        free_route = self.get_free_channels()
        if len(free_route) > 0:
            for i in free_route:
                self.states[i] = 1
                self.next_event_times[i] = self.current_time + super().get_delay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure_count += 1

    def out_act(self):
        current_channel = self.get_current_channel()
        for i in current_channel:
            super().out_act()
            self.next_event_times[i] = np.inf
            self.states[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.states[i] = 1
                self.next_event_times[i] = self.current_time + self.get_delay()
            if self.next_element is not None:
                next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.in_act()

    def get_free_channels(self):
        free_channels = []
        for i in range(self.channels_count):
            if self.states[i] == 0:
                free_channels.append(i)

        return free_channels

    def get_current_channel(self):
        current_channels = []
        for i in range(self.channels_count):
            if self.next_event_times[i] == self.current_time:
                current_channels.append(i)
        return current_channels

    def print_info(self):
        super().print_info()
        print(f'failure = {str(self.failure_count)}, queue_length = {str(self.queue)}')

    def calculate(self, delta):
        self.mean_queue += self.queue * delta

        if self.queue > self.max_observed_queue:
            self.max_observed_queue = self.queue

        for i in range(self.channels_count):
            self.mean_load += self.states[i] * delta

        self.mean_load = self.mean_load / self.channels_count
