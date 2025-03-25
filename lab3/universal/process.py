import numpy as np
from shared import element as e


class Process(e.Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.t_next = [np.inf] * self.channel
        self.state = [0] * self.channel

    def in_act(self):
        free_route = self.get_free_channels()
        if len(free_route) > 0:
            for i in free_route:
                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def out_act(self):
        current_channel = self.get_current_channel()
        for i in current_channel:
            super().out_act()
            self.t_next[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.t_next[i] = self.t_curr + self.get_delay()
            if self.next_element is not None:
                next_element = self.choose_next_element()
                next_element.in_act()
