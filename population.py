import numpy as np

class Population:
    def __init__(self, n_, k_):
        self.n = n_
        self.k = k_
        first_gen = np.ones(self.n)

        self.last_live_gen = {}
        for i in range(self.k):
            self.last_live_gen[i] = 0
        counter = -1
        for i in range(first_gen.shape[0]):
            if (i % int(self.n / self.k)) == 0 and counter+1 != self.k:
                #print("Incrementing: ", counter, i)
                counter += 1
            first_gen[i] = counter
        self.num_unique = self.k
        self.current_gen = first_gen
        self.gen_idx = 0
        self.generations = np.zeros((2*self.n, self.k))
        self.generations[self.gen_idx] = self.get_genotype_counts()

    def run(self, display_stats=False):
        while self.num_unique > 1:
            self.generation()
        if display_stats:
            self.display_generation_dists()
        self.derive_and_set_beginning_of_domination()

    def get_genotype_counts(self):
        uni, counts = np.unique(self.current_gen, return_counts=True)
        self.num_unique = uni.shape[0]
        result = np.zeros(self.k, dtype=int)
        # print(uni, counts, result)
        for i, j in zip(uni.astype(int), counts.astype(int)):
            # print(i, j)
            result[i] = j
        return result

    def generation(self, display_first_gens=False):
        child_is_of = np.random.randint(0, self.n, size=self.n)
        children = np.zeros(self.n).astype(int)
        self.gen_idx += 1
        # Too many gens have passed, copy into a new, bigger array
        if self.gen_idx >= self.generations.shape[0]:
            new_gens = np.zeros(((self.generations.shape[0] + 100), self.k))
            new_gens[0:self.generations.shape[0]] = self.generations
            self.generations = new_gens
        # Create new child array and update age of living genotypes
        # in next gen
        for i in range(self.n):
            children[i] = self.current_gen[child_is_of[i]]
            self.last_live_gen[children[i]] = self.gen_idx
        self.current_gen = children
        self.generations[self.gen_idx] = self.get_genotype_counts()
        if self.gen_idx < 5 and display_first_gens:
            self.display_generation_dist()

    def display_generation_dist(self):
        from scipy.stats import mode
        import matplotlib.pyplot as plt
        guid = np.random.randint(1000000)
        plt.figure(guid)
        print("Mode", mode(self.current_gen))
        n_bins = self.n
        # Generate a normal distribution, center at x=0 and y=5
        x = self.current_gen
        # y = .4 * x + np.random.randn(100000) + 5
        fig, axs = plt.subplots(tight_layout=True)
        # We can set the number of bins with the `bins` kwarg
        axs.hist(x, bins=n_bins)
        plt.title("Evenly Distributed Start: {0}\nChild Distribution Generation {1}".format(self.k, self.gen_idx))
        #plt.show()

    def display_generation_dists(self):
        import matplotlib.pyplot as plt
        guid = np.random.randint(1000000)
        plt.figure(guid)
        lines = self.generations[:self.gen_idx].T
        #print("First start: ", lines[:, 0])
        names = [str(x) for x in np.arange(self.k)]
        x = np.arange(self.gen_idx)
        for i in range(self.k):
            plt.plot(x, lines[i], '-', label=names[i])

        plt.title("Evenly Distributed Start: {0}".format(self.k))
        plt.savefig("outputs/generation_tracking_{0}_{1}.png".format(self.k, guid))
        #plt.show()

    def derive_and_set_beginning_of_domination(self):
        # Get last intersection by running through the generations backwards
        # until a point is reached where the ultimately winning genotype is
        # not greater than all others.
        idx = self.gen_idx
        winner = -1
        for i in range(self.k):
            if self.generations[self.gen_idx][i] > 0:
                winner = i
        assert(winner != -1)
        is_strictly_greatest = True
        while is_strictly_greatest and idx >= 0:
            for i in range(self.k):
                if i != winner and self.generations[idx][i] >= self.generations[idx][winner]:
                    is_strictly_greatest = False
            idx -= 1
        self.beginning_of_domination = idx
        return self.beginning_of_domination
