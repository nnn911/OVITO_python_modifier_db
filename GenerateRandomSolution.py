# OVITO Pro 3.4.0

from ovito.data import *
import numpy as np


def modify(frame: int, data: DataCollection, conc=(0.5, 0.5), seed=123456):
    assert np.isclose(np.sum(conc), 1), f'sum conc = {np.sum(conc)} != 1'

    # new np syntax (currently not supported by ovito)
    # rng = np.random.default_rng(seed)
    np.random.seed = seed

    conc_vec = []
    for i, c in enumerate(conc):
        conc_vec += ([i+1]*int(data.particles.count*c))

    x_p = np.cumsum(conc)
    while len(conc_vec) < data.particles.count:
        # conc_vec.append(np.sum(x_p < rng.random())+1)
        conc_vec.append(np.sum(x_p < np.random.random())+1)

    conc_vec = np.array(conc_vec)
    np.random.shuffle(conc_vec)
    # rng.shuffle(conc_vec)

    data.particles_['Particle Type_'][...] = conc_vec
    pt, count = np.unique(conc_vec, return_counts=True)
    count = count / np.sum(count)
    print('New concentrations:')
    for p, c in zip(pt, count):
        print(f'Type {p}: {c}')
