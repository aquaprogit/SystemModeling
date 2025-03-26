import numpy as np

from element import Element


class Process(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_times = [np.inf] * self.channels_count
        self.states = [0] * self.channels_count

    def enter(self):
        free_route = self.get_free_channels()
        if len(free_route) > 0:
            for i in free_route:
                self.states[i] = 1
                self.next_times[i] = self.current_time + super().get_delay()
                break
        else:
            if self.queue_len < self.max_queue_len:
                self.queue_len += 1
            else:
                self.failure_quantity += 1

    def leave(self):
        current_channel = self.get_current_channels()
        for i in current_channel:
            super().leave()
            self.next_times[i] = np.inf
            self.states[i] = 0
            if self.queue_len > 0:
                self.queue_len -= 1
                self.states[i] = 1
                self.next_times[i] = self.current_time + self.get_delay()
            if self.next_element is not None:
                next_element = self.choose_next_element()
                next_element.enter()
