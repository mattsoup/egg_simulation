#!/usr/bin/env python
""" This is a simple simulation of symbiont transmission to cicada eggs """

import numpy
import sys
import time
import multiprocessing as mp


if len(sys.argv) != 6:
    print "Usage: ./mp_egg_model.py <number of Hodg. lineages> \
          <Number of Hodg. cells passed to eggs> <Number of eggs laid> \
          <# of processes> <outfile prefix>\n"
    quit()

num_hodg = int(sys.argv[1])
num_cells = int(sys.argv[2])
num_eggs_laid = int(sys.argv[3])
num_processes = int(sys.argv[4])
outprefix = sys.argv[5]
out = open(outprefix + ".out", "w")
temp_out = open("mytemp", "w")
temp_output = mp.Queue()

# This chooses a random list of coverage values
#covg = numpy.random.randint(1, high = 1000, size = num_hodg)

# This will allow all lineages to have equal coverage
#covg = [1] * num_hodg

# this is 30 covg values that are close to magtre hodg. values
#covg = [181, 273, 673, 110, 259, 57, 126, 145, 209, 227, 132, 70, 91, 83, 481, 88, 120, 407, 863, 205, 193, 111, 92, 140, 140, 144, 110, 50, 100, 75]

# this is 50 covg values that are close to magtre hodg. values
#covg = [181, 234, 658, 110, 233, 55, 139, 87, 194, 192, 123, 67, 86, 73, 476, 81, 106, 478, 34, 177, 421, 151, 26, 8, 72, 50, 441, 102, 118, 695, 123, 38, 90, 108, 96, 59, 430, 424, 74, 109, 50, 117, 394, 60, 490, 145, 530, 100, 204, 158]

# this is the covg values for the 30 finished circles from the current biology paper (magtre)
#covg = [384,504,1392,1419,925,1043,233,503,116,155,291,401,184,421,425,57,19,262,144,256,184,157,115,1136,175,229,223,344,99,84]

#And finally coverage values for Tettigades species
covg = [0.546438975,0.160966243,0.160528124,0.091050972,0.007917124,0.033098563] #T. chilensis TETCHI
#covg = [0.415265231,0.223064789,0.210425656,0.076773736,0.049476574,0.024994014] #T. auropilosa TETAUR
#covg = [0.779348307,0.093756099,0.065020762,0.055048066,0.006826765] #T. limbata TETLIM
#covg = [0.590751276,0.282854694,0.12639403] #T. undata TETLON
#covg = [0.61148882,0.38851118] #T. undata TETUND

# this sorts the coverage list so it will be more even, though idk if it's necessary
covg = sorted(covg)

# this sorts the coverage list (in reverse) so it will be more even, though idk if it's necessary
#covg = sorted(covg, reverse=True)

print covg
unique = numpy.unique


def min_1(num_hodg, num_cells, num_eggs_laid, covg, temp_output):
    """ A function to calculate the proportion of eggs that receive all
    Hodgkinia lineages.
    """

    viable = 0
    viable_list = []
    for x in xrange(0, num_eggs_laid):
        genome = numpy.random.choice(num_hodg, size = num_cells, p = covg)
        uniq, counts = unique(genome, return_counts = True)
        uniq = uniq.tolist()
        counts = counts.tolist()
        if len(uniq) == num_hodg:
            viable += 1
    viable_list.append(num_hodg)
    viable_list.append(num_cells)
    viable_list.append(float(viable) / num_eggs_laid)
    print "Hodg: %s Cells: %s Percent viable: %s" % (num_hodg, num_cells, float(viable) / num_eggs_laid)
    return viable_list


def diff_min(num_hodg, num_cells, num_eggs_laid, covg, temp_output):
    """ This function is similar to 'min_1', except it allows for a minimum number
    of Hodgkinia cells (variable 'min') transmitted to all eggs
    """

    min = 100
    viable = 0
    viable_list = []
    for x in xrange(0, num_eggs_laid):
        genome = numpy.random.choice(num_hodg, size = num_cells, p = covg)
        uniq, counts = unique(genome, return_counts = True)
        uniq = uniq.tolist()
        counts = counts.tolist()
        if len(uniq) == num_hodg and all(x >= min for x in counts):
            viable += 1
    viable_list.append(num_hodg)
    viable_list.append(num_cells)
    viable_list.append(float(viable) / num_eggs_laid)
    print "Hodg: %s Cells: %s Percent viable: %s" % (num_hodg, num_cells, float(viable) / num_eggs_laid)
    return viable_list


percents = []


def test_num_hodg(*list_of_indices):
    """ This function takes the list of indices that each process is responsible
    for. It calculates the portion of the coverage list needed, and for each
    number of Hodgkinia cells runs 'diff_min' or 'min_1' (hard coded)
    """

    print list_of_indices
    for index in list_of_indices:
        slice_covg = covg[:(index + 1)]
        new_sum = sum(slice_covg)
        slice_covg = [(float(item) / new_sum) for item in slice_covg]
        for y in xrange(1, (num_cells + 1), 20):
            viable_list = diff_min((index + 1), y, num_eggs_laid, slice_covg,
                                   temp_output)
            percents.append(viable_list)
            if viable_list[2] == 1.0:
                print "skipping %s, cells %s - %s" % ((index + 1), y + 20,
                                                      (num_cells + 1))
                for z in xrange(y + 20, (num_cells + 1), 20):
                    percents.append([(index + 1), z, 1.0])
                break
        temp_output.put(percents)
        to_write(temp_output)


def to_write(temp_output):
    """A simple function to write the results in real time"""

    covgs = []
    covgs.append(temp_output.get())
    for item in covgs:
        for thing in item:
            temp_out.write("%s %s %s\n" % (thing[0], thing[1], thing[2]))
    temp_out.flush()
    covgs = []


processes = []
prev_end = 0
indices = {}
for x in range(num_processes):
    indices[str(x)] = []

x = 0
y = 0

while x < num_hodg:
    indices[str(y)].append(x)
    y += 1
    x += 1
    if y == num_processes:
        y = 0

for item in indices:
    processes.append(mp.Process(target = test_num_hodg, args = indices[item]))

for p in processes:
    p.daemon = True
    p.start()

covgs = []
for p in processes:
    while p.is_alive() == True:
        pass
        print "checking %s" % p
        time.sleep(5)
    p.join()

temp_out.close()
out_set = set()
temp_out = open("mytemp", "r")
for line in temp_out:
    out_set.add(line)

for line in sorted(out_set):
    out.write(line)
