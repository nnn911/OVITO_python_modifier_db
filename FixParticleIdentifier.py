# OVITO Pro 3.4.0

from ovito.data import *


def modify(frame: int, data: DataCollection, init_val=1):
    new_ids = list(range(init_val, data.particles.count+init_val))
    data.particles_['Particle Identifier_'][...] = new_ids
