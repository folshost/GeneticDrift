import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mode


def get_unique(arr):
    uniques = {}
    for i in arr:
        if i in uniques:
            uniques[i] += 1
        else:
            uniques[i] = 1
    return uniques

sample_size = 2
n = 1000

times = []
last_iterations = []
for j in range(sample_size):
    last_iteration = {}
    for i in np.zeros(n).astype(int):
        last_iteration[i] = 0
    # children = np.random.randint(n, size=n).astype(int)
    children = np.arange(n).astype(int)
    #print("Initial children ", children)
    iteration_num = 0
    while(len(get_unique(children).keys()) > 1):
        iteration_num += 1
        parents = children
        child_is_of = np.random.randint(0, n, size=n)
        children = np.zeros(n).astype(int)
        #print("Shape: ", child_is_of.shape)
        for i in range(len(child_is_of)):
            children[i] = parents[child_is_of[i]]
            # print(children[i])
            last_iteration[children[i]] = iteration_num
        if iteration_num == 1:
            print("Last iteration", last_iteration)
        if iteration_num < 5 and j == 0:
            # print(child_is_of, children)
            print("Mode", mode(child_is_of))
            n_bins = 1000
            # Generate a normal distribution, center at x=0 and y=5
            x = child_is_of
            # y = .4 * x + np.random.randn(100000) + 5
            fig, axs = plt.subplots(tight_layout=True)
            # We can set the number of bins with the `bins` kwarg
            axs.hist(x, bins=n_bins)
            plt.title("Child Distribution Generation {0}".format(iteration_num))
            plt.show()

    print("It took {0} generations. Dominant {1}.".format(iteration_num, children[0]))
    times += [iteration_num]
    last_iterations += [np.sort(last_iteration)]
print("Resulting iterations: ")
print(times)
#print(last_iterations[:2])
print("Last iteration mode: ", mode(last_iterations[0]))
print(np.std(times), np.mean(times))

n_bins = 2000

# Generate a normal distribution, center at x=0 and y=5
x = last_iterations[0]
# y = .4 * x + np.random.randn(100000) + 5

fig, axs = plt.subplots(tight_layout=True)

# We can set the number of bins with the `bins` kwarg
axs.hist(x, bins=n_bins)
plt.show()
