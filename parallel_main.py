import multiprocessing
import numpy as np
import sys
import time
from joblib import Parallel, delayed
from population import Population


def get_time_and_domination(n, k):
    pop = Population(n, k)
    pop.run(display_stats=display_stats)
    # print(k, pop.gen_idx+1)
    time = pop.gen_idx
    beginning = pop.beginning_of_domination
    return time, beginning

if len(sys.argv) < 3:
    assert False, "usage: {0} uppermost_k_value sample_size".format(sys.argv[0])
sample_size = int(sys.argv[2])
n = 1000
figure_ = 0
display_stats = False
num_cores = multiprocessing.cpu_count()
print("Number of available cores: ", num_cores)
k_times = []
for k in range(2, int(sys.argv[1])):
    start_time = time.time()
    
    file_name = "results/genetic_drift_{0}_{1}.dat".format(k, sample_size)
    times = np.arange(sample_size, dtype=int)
    generations = Parallel(n_jobs=num_cores)(delayed(get_time_and_domination)(n, k) for i in times)
    times = np.array([i for i, j in generations])
    last_domination_fractions = np.array([(i-j)/i for i, j in generations])
    dominations = np.array([j for i, j in generations])
    k_times += [(k, times.mean(), times.std(),    \
                last_domination_fractions.mean(), \
                last_domination_fractions.std(), times, dominations, \
                last_domination_fractions)]
    # Open a file
    fo = open(file_name, "w")
    fo.write(str(k_times[k-2][0])+"\t")
    fo.write(str(k_times[k-2][1])+"\t")
    fo.write(str(k_times[k-2][2])+"\t")
    fo.write(str(k_times[k-2][3])+"\n")
    fo.write(str(k_times[k-2][4])+"\n")
    fo.write(str(k_times[k-2][5])+"\n")
    fo.write(str(k_times[k-2][6])+"\n")
    # Close opend file
    fo.close()
    #print(k_times[k-2])
    print("Execution time for k = {0}: {1} seconds".format(k, time.time() - start_time))

