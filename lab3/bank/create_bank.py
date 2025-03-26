from shared import element as e


class CreateBank(e.Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def out_act(self):
        super().out_act()
        
        self.t_next[0] = self.t_curr + super().get_delay()

        p1 = self.next_element[0]
        p2 = self.next_element[1]

        if p1.queue <= p2.queue:
            p1.in_act()
        else:
            p2.in_act()
