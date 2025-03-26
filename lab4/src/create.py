from element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def leave(self):
        super().leave()
        self.next_times[0] = self.current_time + super().get_delay()

        next_element = self.choose_next_element()
        next_element.enter()
