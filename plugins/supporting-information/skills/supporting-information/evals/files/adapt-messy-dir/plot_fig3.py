import os
import numpy as np
import matplotlib.pyplot as plt

def rdf(r, nbins, rmax, volume):
    # radial distribution from pair distances
    hist, edges = np.histogram(r, bins=nbins, range=(0, rmax))
    shell = 4 / 3 * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    n = len(r)
    return 0.5 * (edges[1:] + edges[:-1]), hist / shell / (n / volume)


r = np.loadtxt(os.path.join('/home/jane/sims/lyso-nacl/run', 'distances.dat'))
x, g = rdf(r, 150, 3.0, 1000.0)
f = open('fig3_values.txt', 'w')
for xi, gi in zip(x, g):
    f.write(f'{xi} {gi}\n')
plt.plot(x, g)
plt.savefig('fig3.png')
