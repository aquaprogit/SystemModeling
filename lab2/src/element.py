import fun_rand as fun

class Element:
    nextId = 0

    def __init__(self, delay=None, distribution=None):
        self.next_event_times = [0]
        self.delay_mean = delay
        self.delay_deviation = None
        self.quantity = 0
        self.current_time = self.next_event_times
        self.states = [0]
        self.next_element = None
        self.id = Element.nextId
        Element.nextId += 1
        self.name = 'Element' + str(self.id)
        self.distribution = distribution
        self.probabilities = [1]

    def get_delay(self):
        if self.distribution == 'exp':
            return fun.exp(self.delay_mean)
        elif self.distribution == 'norm':
            return fun.norm(self.delay_mean, self.delay_deviation)
        elif self.distribution == 'uniform':
            return fun.uniform(self.delay_mean, self.delay_deviation)
        return self.delay_mean

    def in_act(self):
        pass

    def get_states(self):
        return self.states

    def set_states(self, state_values):
        self.states = state_values

    def set_next_event_times(self, t_next_new):
        self.next_event_times = t_next_new

    def get_current_time(self):
        return self.current_time

    def out_act(self):
        self.quantity += 1

    def result(self):
        print(f'{self.name} quantity = {self.quantity} state = {self.states}')

    def print_info(self):
        print(f'{self.name} state = {self.states} quantity = {self.quantity} t_next = {self.next_event_times}')

    def calculate(self, delta):
        pass

    def calculate_mean(self, delta):
        pass
