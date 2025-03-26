from create import Create
from model import Model
from process import Process
import random

class ModelBuilder:
    def __init__(self):
        pass

    def build(self, n: int):
        pass


class SimpleModelBuilder(ModelBuilder):
    def __init__(self):
        super().__init__()

    def build(self, n: int):
        c1 = Create(delay_mean=random.randint(1, 5), name='CREATOR', distribution='exp')
        p_prev = c1
        elements = [c1]
        for i in range(n - 1):
            p = Process(delay_mean=random.randint(1, 5), distribution='exp')
            p_prev.next_element = [p]
            elements.append(p)
            p_prev = p
        p = Process(channels_count=2, delay_mean=random.randint(1, 5), distribution='exp')
        p_prev.next_element = [p]
        elements.append(p)
        model = Model(elements)
        return c1, model

class ComplexModelBuilder(ModelBuilder):
    def __init__(self):
        super().__init__()

    def build(self, n: int):
        c1 = Create(delay_mean=random.randint(1, 5), name='CREATOR', distribution='exp')
        p_prev = c1
        elements = [c1]
        for i in range(int(n / 5)):
            p = Process(delay_mean=random.randint(1, 5), distribution='exp')
            p_prev.next_element = [p]
            p1 = Process(delay_mean=random.randint(1, 5), distribution='exp')
            p2 = Process(delay_mean=random.randint(1, 5), distribution='exp')
            p.next_element = [p1, p2]
            p.probabilities = [0.7, 0.3]
            if i != int(n / 5) - 1:
                p3 = Process(delay_mean=random.randint(1, 5), distribution='exp')
                p1.next_element = [p3]
                p2.next_element = [p3]
                p4 = Process(delay_mean=random.randint(1, 5), distribution='exp')
                p3.next_element = [p4]
                p_prev = p4
                elements.append(p)
                elements.append(p1)
                elements.append(p2)
                elements.append(p3)
                elements.append(p4)
            else:
                p3 = Process(channels_count=2, delay_mean=random.randint(1, 5), distribution='exp')
                p1.next_element = [p3]
                p2.next_element = [p3]
                elements.append(p)
                elements.append(p1)
                elements.append(p2)
                elements.append(p3)
                p3.channels_count = 2
        model = Model(elements)
        return c1, model
