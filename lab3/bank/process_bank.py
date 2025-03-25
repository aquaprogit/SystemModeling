import numpy as np
from shared import element as e


class ProcessBank(e.Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.t_next = [np.inf] * self.channel
        self.state = [0] * self.channel
        self.delta_t_departure = 0
        self.tprev_departure = 0
        self.delta_t_in_bank = 0
        self.tprev_in_bank = 0

    def in_act(self):
        free_route = self.get_free_channels()
        if len(free_route) > 0:
            for i in free_route:
                self.tprev_in_bank = self.t_curr
                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
                break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def out_act(self):
        super().out_act()
        current_channel = self.get_current_channel()
        for i in current_channel:

            self.t_next[i] = np.inf
            self.state[i] = 0

            # обраховуємо середній інтервал часу між від'їздами клієнтів від вікон
            self.delta_t_departure += self.t_curr - self.tprev_departure
            self.tprev_departure = self.t_curr

            # обраховуємо середній час перебування клієнта в банку
            self.delta_t_in_bank = + self.t_curr - self.tprev_in_bank

            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
            if self.next_element is not None:
                next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.in_act()
