from shared.element import Element


class ElementHospital(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_type = None

    def get_delay(self):
        # умови на час реєстрації хворих різних типів
        if self.name == 'RECEPTION':
            if self.current_type == 1:
                self.delay_mean = 15
            elif self.current_type == 2:
                self.delay_mean = 40
            elif self.current_type == 3:
                self.delay_mean = 30
        return super().get_delay()

    def in_act(self, next_type_element, t_start):
        pass
