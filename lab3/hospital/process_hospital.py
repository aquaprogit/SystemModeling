import numpy as np

from hospital.element_hospital import ElementHospital


class ProcessHospital(ElementHospital):
    def __init__(self, required_path=None, **kwargs):
        super().__init__(**kwargs)

        # масив типів хворих, які знаходяться на кожному каналі
        self.types = [-1] * self.channel
        # масив типів хворих, які знаходяться в черзі
        self.queue_types = []
        # шлях, в залежності від типу хворого
        self.required_path = required_path
        # пріоритетний тип хворого
        self.prior_types = []

        self.delta_t_following_to_the_lab_reception = 0
        self.tprev_following_to_the_lab_reception = 0

        self.t_starts = [-1] * self.channel
        self.t_starts_queue = []

        self.delta_t_finished2_new = 0
        self.type2_cnt_new = 0

    def in_act(self, next_type_element, t_start):
        self.current_type = next_type_element

        if self.name == 'FOLLOWING_TO_THE_LAB_RECEPTION':
            self.delta_t_following_to_the_lab_reception += self.t_curr - self.tprev_following_to_the_lab_reception
            self.tprev_following_to_the_lab_reception = self.t_curr

        if self.name == 'FOLLOWING_TO_THE_RECEPTION' and next_type_element == 2:
            self.delta_t_finished2_new += self.t_curr - t_start
            self.type2_cnt_new += 1

        free_channels = self.get_free_channels()
        for i in free_channels:
            self.state[i] = 1

            self.t_next[i] = self.t_curr + super().get_delay()
            self.types[i] = self.current_type
            self.t_starts[i] = t_start
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
                self.queue_types.append(self.current_type)
                self.t_starts_queue.append(t_start)
                if self.queue > self.max_observed_queue:
                    self.max_obs_queue_length = self.queue
            else:
                self.failure += 1

    def out_act(self):
        super().out_act()

        current_channels = self.get_current_channel()

        for i in current_channels:
            self.t_next[i] = np.inf
            self.state[i] = 0
            prev_type = self.types[i]
            prev_t_start = self.t_starts[i]
            self.types[i] = -1
            self.t_starts[i] = -1

            if self.queue > 0:
                self.queue -= 1
                prior_index = self.get_prior_index_from_queue()
                self.current_type = self.queue_types.pop(prior_index)

                self.state[i] = 1
                self.t_next[i] = self.t_curr + super().get_delay()
                self.types[i] = self.current_type
                self.t_starts[i] = self.t_starts_queue.pop(prior_index)
            if self.next_element is not None:
                self.current_type = 1 if self.name == 'FOLLOWING_TO_THE_RECEPTION' else prev_type

                #                 print('next_type_element:', self.next_type_element)
                if self.required_path is None:
                    #                     print('in if req path')
                    next_element = np.random.choice(self.next_element, p=self.probability)
                    next_element.in_act(self.current_type, prev_t_start)
                else:
                    for idx, path in enumerate(self.required_path):
                        #                         print('Path:', path)
                        if self.current_type in path:
                            next_element = self.next_element[idx]
                            #                             print(f'\n\nWe have type {self.next_type_element} and go to the {next_element.name}\n\n')
                            next_element.in_act(self.current_type, prev_t_start)
                            break

    def get_prior_index_from_queue(self):
        for prior in self.prior_types:
            for type_i in np.unique(self.queue_types):
                if type_i == prior:
                    return self.queue_types.index(type_i)
        else:
            return 0

    def print_info(self):
        super().print_info()
        print(f'queue={self.queue}; failure={self.failure}')
        print(f'types of elements={self.types}')

    def calculate(self, delta):
        self.mean_queue_length = + delta * self.queue
