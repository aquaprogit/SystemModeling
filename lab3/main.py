from bank.create_bank import CreateBank
from bank.model_bank import ModelBank
from bank.process_bank import ProcessBank
from shared import fun_rand as fun
from hospital.create_hospital import CreateHospital
from hospital.dispose_hospital import DisposeHospital
from hospital.model_hospital import ModelHospital
from hospital.process_hospital import ProcessHospital
from universal.create import Create
from universal.model import Model
from universal.process import Process


def channel_model():
    print('Channel model')
    c1 = Create(delay_mean=5, name='CREATOR', distribution='exp')
    p1 = Process(max_queue=3, n_channel=2, delay_mean=5, distribution='exp')

    c1.next_element = [p1]
    elements = [c1, p1]
    model = Model(elements)
    model.simulate(1000)


def simple_model():
    print('Simple model')
    c1 = Create(delay_mean=5, name='CREATOR', distribution='exp')
    p1 = Process(max_queue=3, delay_mean=5, distribution='exp')

    c1.next_element = [p1]
    elements = [c1, p1]
    model = Model(elements)
    model.simulate(1000)


def probability_model():
    print('Probability model')
    p1 = Process(max_queue=3, delay_mean=5, distribution='exp')

    p1.probability = [0.9, 0.1]
    base_model(p1)


def priority_model():
    print('Priority model')
    p1 = Process(max_queue=3, delay_mean=5, distribution='exp')
    p1.priority = [2, 1]

    base_model(p1)


def base_model(p1):
    c1 = Create(delay_mean=5, name='CREATOR', distribution='exp')
    p2 = Process(max_queue=3, delay_mean=5, distribution='exp')
    p3 = Process(max_queue=3, delay_mean=5, distribution='exp')

    c1.next_element = [p1]
    p1.next_element = [p2, p3]
    elements = [c1, p1, p2, p3]
    model = Model(elements)
    model.simulate(1000)


def bank_model():
    print('Bank model')
    c1 = CreateBank(delay_mean=0.5, name='CREATOR', distribution='exp')
    p1 = ProcessBank(max_queue=3, delay_mean=0.3, name='CASHIER_1', distribution='exp')
    p2 = ProcessBank(max_queue=3, delay_mean=0.3, name='CASHIER_2', distribution='exp')

    c1.next_element = [p1, p2]

    # Обидва касири зайняті
    p1.state[0] = 1
    p2.state[0] = 1

    # Тривалість
    # обслуговування для кожного касира нормально розподілена з
    # математичним очікуванням, рівним 1 од. часу, і середньоквадратичним
    # відхиленням, рівним 0,3 од. часу
    p1.t_next[0] = fun.norm(1, 0.3)
    p2.t_next[0] = fun.norm(1, 0.3)

    # Прибуття першого клієнта заплановано на момент часу 0,1 од. часу
    c1.t_next[0] = 0.1

    # У кожній черзі очікують по два автомобіля.
    p1.queue = 2
    p2.queue = 2

    element_list = [c1, p1, p2]
    bank = ModelBank(element_list, balancing=[p1, p2])
    bank.simulate(1000)


def hospital_model():
    print('Hospital model')
    c1 = CreateHospital(delay_mean=15.0, name='CREATOR_1', distribution='exp')
    p1 = ProcessHospital(max_queue=100, n_channel=2, name='RECEPTION', distribution='exp')
    p2 = ProcessHospital(max_queue=100, delay_mean=3.0, delay_dev=8, n_channel=3, name='FOLLOWING_TO_THE_WARD',
                         distribution='unif')
    p3 = ProcessHospital(max_queue=0, delay_mean=2.0, delay_dev=5, n_channel=10, name='FOLLOWING_TO_THE_LAB_RECEPTION',
                         distribution='unif')
    p4 = ProcessHospital(max_queue=100, delay_mean=4.5, delay_dev=3, n_channel=1, name='LAB_REGISTRY',
                         distribution='erlang')
    p5 = ProcessHospital(max_queue=100, delay_mean=4.0, delay_dev=2, n_channel=2, name='EXAMINATION',
                         distribution='erlang')
    p6 = ProcessHospital(max_queue=0, delay_mean=2.0, delay_dev=5, n_channel=10, name='FOLLOWING_TO_THE_RECEPTION',
                         distribution='unif')

    d1 = DisposeHospital(name='EXIT1')
    d2 = DisposeHospital(name='EXIT2')

    c1.next_element = [p1]
    p1.next_element = [p2, p3]
    p2.next_element = [d1]
    p3.next_element = [p4]
    p4.next_element = [p5]
    p5.next_element = [d2, p6]
    p6.next_element = [p1]

    p1.prior_types = [1]

    p1.required_path = [[1], [2, 3]]
    p5.required_path = [[3], [2]]

    elements = [c1, p1, p2, p3, p4, p5, p6, d1, d2]

    model = ModelHospital(elements)
    model.simulate(1000)


def main():
    continue_test = "Press Enter to continue..."
    # simple_model()
    # input(continue_test)
    # channel_model()
    # input(continue_test)
    # probability_model()
    # input(continue_test)
    # priority_model()
    # input(continue_test)
    # bank_model()
    # input(continue_test)
    hospital_model()


if __name__ == "__main__":
    main()
