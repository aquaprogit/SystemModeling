from create import Create
from tabulate import tabulate
from model import Model
from process import Process
import pandas as pd


c = Create(5)

p1 = Process(5)
p2 = Process(5)
p3 = Process(5)

c.next_element = [p1]
p1.next_element = [p2, p3]

p1.probability = ([0.5, 0.5])

p1.max_queue = 5
p2.max_queue = 5
p3.max_queue = 5

c.distribution = 'exp'
p1.distribution = 'exp'
p2.distribution = 'exp'
p3.distribution = 'exp'

c.name = 'Creator'
p1.name = 'Process 1'
p2.name = 'Process 2'
p3.name = 'Process 3'

elements = [c, p1, p2, p3]
model = Model(elements)
res = model.simulate(1000)

# c = Create(5)

# p1 = Process(5)

# p1.max_queue = 5

# c.distribution = 'exp'
# p1.distribution = 'exp'

# c.name = 'Creator'
# p1.name = 'Process 1'

# c.next_element = [p1]

# elements = [c, p1]
# model = Model(elements)
# res = model.simulate(1000)

# c = Create(5)

# p1 = Process(5, 2)

# p1.max_queue = 5

# c.distribution = 'exp'
# p1.distribution = 'exp'

# c.name = 'Creator'
# p1.name = 'Process 1'

# c.next_element = [p1]

# elements = [c, p1]
# model = Model(elements)
# res = model.simulate(1000)


# n_param = 15

# create_delays =      [4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4, 4, 4, 4]
# process1_delays =    [4, 4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4, 4, 4]
# process2_delays =    [4, 4, 4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4, 4]
# process3_delays =    [4, 4, 4, 4, 10, 4, 4, 4, 4, 4, 4, 0.5, 4, 4, 4]
# process1_max_queue = [5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5, 5]
# process2_max_queue = [5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1, 5]
# process3_max_queue = [5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 1]
# distribution = 'exp'

# df = pd.DataFrame()
# rows = []

# for i in range(n_param):
#     c = Create(create_delays[i])

#     p1 = Process(process1_delays[i])
#     p2 = Process(process2_delays[i])
#     p3 = Process(process3_delays[i])

#     p1.max_queue = process1_max_queue[i]
#     p2.max_queue = process2_max_queue[i]
#     p3.max_queue = process3_max_queue[i]

#     c.distribution = distribution
#     p1.distribution = distribution
#     p2.distribution = distribution
#     p3.distribution = distribution

#     c.name = 'Creator'
#     p1.name = 'Process 1'
#     p2.name = 'Process 2'
#     p3.name = 'Process 3'

#     c.next_element = [p1]
#     p1.next_element = [p2]
#     p2.next_element = [p3]

#     elements = [c, p1, p2, p3]
#     model = Model(elements)
#     res = model.simulate(1000)

#     param = {'create_delays': create_delays[i],
#              'process1_delays': process1_delays[i],
#              'process2_delays': process2_delays[i],
#              'process3_delays': process3_delays[i],
#              'process1_max_queue': process1_max_queue[i],
#              'process2_max_queue': process2_max_queue[i],
#              'process3_max_queue': process3_max_queue[i],
#              'process1_processed': p1.quantity,
#              'process1_failed': p1.failure,
#              'process2_processed': p2.quantity,
#              'process2_failed': p2.failure,
#              'process3_processed': p3.quantity,
#              'process3_failed': p3.failure,
#              'distribution': distribution}

#     rows.append({**param, **res})

# df = df.append(rows)
# df.to_excel('result.xlsx')
# print(tabulate(df, headers='keys', tablefmt='fancy_grid', numalign="center"))
