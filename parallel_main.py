import multiprocessing
import numpy as np
from joblib import Parallel, delayed
from population import Population


def get_time_and_domination(n, k):
    pop = Population(n, k)
    pop.run(display_stats=display_stats)
    # print(k, pop.gen_idx+1)
    time = pop.gen_idx
    beginning = pop.beginning_of_domination
    return time, beginning


sample_size = 100
n = 1000
figure_ = 0
display_stats = False

k_times = []
for k in range(2, 5):
    times = np.zeros(sample_size, dtype=int)
    num_cores = multiprocessing.cpu_count()
    generations = Parallel(n_jobs=num_cores)(delayed(get_time_and_domination)(n, k) for i in times)
    times = np.array([i for i, j in generations])
    last_domination_fractions = np.array([(i-j)/i for i, j in generations])
    k_times += [(k, times.mean(), last_domination_fractions.mean(), last_domination_fractions.std())]
print(k_times)

