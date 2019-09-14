import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mode


class Population:
    def __init__(self, n_, k_):
        self.n = n_
        self.k = k_
        first_gen = np.zeros(self.n)
        counter = 0
        first_gen[0] = counter
        self.last_live_gen = {}
        for i in range(self.k):
            self.last_live_gen[i] = 0
        for i in range(1, first_gen.shape[0]):
            if (self.n - i) % (self.n / self.k) == 0 and counter != k:
                counter += 1
            first_gen[i] = counter
        self.num_unique = self.k
        self.current_gen = first_gen
        self.gen_idx = 0
        self.generations = np.zeros((2*self.n, self.k))
        self.generations[self.gen_idx] = self.get_count_arr()

    def run(self, display_stats=False):
        while self.num_unique > 1:
            self.generation(display_stats)


    def get_count_arr(self):
        uni, counts = np.unique(self.current_gen, return_counts=True)
        self.num_unique = uni.shape[0]
        result = np.zeros(self.k, dtype=int)
        #print(uni, counts, result)
        for i, j in zip(uni.astype(int), counts.astype(int)):
            #print(i)
            result[i] = j
        return result


    def generation(self, display_stats=False):
        child_is_of = np.random.randint(0, self.n, size=self.n)
        children = np.zeros(self.n).astype(int)
        self.gen_idx += 1
        if self.gen_idx >= self.generations.shape[0]:
            new_gens = np.zeros(((self.generations.shape[0] + 100), k))
            new_gens[0:self.generations.shape[0]] = self.generations
            self.generations = new_gens
        for i in range(self.n):
            children[i] = self.current_gen[child_is_of[i]]
            self.last_live_gen[children[i]] = self.gen_idx
        self.current_gen = children
        self.generations[self.gen_idx] = self.get_count_arr()
        if self.gen_idx < 5 and display_stats:
            self.display_stats()

    def display_stats(self):
        print("Mode", mode(self.current_gen))
        n_bins = self.n
        # Generate a normal distribution, center at x=0 and y=5
        x = self.current_gen
        # y = .4 * x + np.random.randn(100000) + 5
        fig, axs = plt.subplots(tight_layout=True)
        # We can set the number of bins with the `bins` kwarg
        axs.hist(x, bins=n_bins)
        plt.title("Evenly Distributed Start: {0}\nChild Distribution Generation {1}".format(self.k, self.gen_idx))
        plt.show()


sample_size = 2
n = 1000

k_times = []
for k in range(2, 5):
    times = np.zeros(sample_size, dtype=int)
    for j in range(sample_size):
        pop = Population(n, k)
        pop.run() #display_stats=(j == 0))
        print("Children: ", pop.generations.T)
        print("It took {0} generations. Dominant {1}.".format(pop.gen_idx+1, pop.current_gen[0]))
        times[j] = pop.gen_idx
    k_times += times.mean()
