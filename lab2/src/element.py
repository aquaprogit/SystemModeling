import fun_rand as fun

class Element:
    nextId = 0

    def __init__(self, delay=None, distribution=None):
        self.t_next = [0]
        self.delay_mean = delay
        self.delay_dev = None
        self.quantity = 0
        self.t_curr = self.t_next
        self.state = [0]
        self.next_element = None
        self.id_el = Element.nextId
        Element.nextId += 1
        self.name = 'Element' + str(self.id_el)
        self.distribution = distribution
        self.probability = [1]

    def get_delay(self):
        if self.distribution == 'exp':
            return fun.exp(self.delay_mean)
        elif self.distribution == 'norm':
            return fun.norm(self.delay_mean, self.delay_dev)
        elif self.distribution == 'uniform':
            return fun.uniform(self.delay_mean, self.delay_dev)
        return self.delay_mean

    def in_act(self):
        pass

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def set_t_next(self, t_next_new):
        self.t_next = t_next_new

    def get_t_curr(self):
        return self.t_curr

    def out_act(self):
        self.quantity += 1

    def result(self):
        print(f'{self.name} quantity = {self.quantity} state = {self.state}')

    def print_info(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} t_next = {self.t_next}')

    def calculate(self, delta):
        pass

    def calculate_mean(self, delta):
        pass
