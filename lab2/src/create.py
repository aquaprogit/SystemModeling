import element as e


class Create(e.Element):
    def __init__(self, delay):
        super().__init__(delay)

    def out_act(self):

        super().out_act()
        
        self.t_next[0] = self.t_curr + self.get_delay()
        self.next_element[0].in_act()
