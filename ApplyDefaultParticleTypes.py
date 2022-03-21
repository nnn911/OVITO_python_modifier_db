from ovito.data import *


def modify(frame: int, data: DataCollection, types=[]):
    atom_types = data.particles_.particle_types_
    for i in range(1, len(types)+1):
        atom_types.type_by_id_(i).name = types[i-1]
        if types[i-1] == 'Mn':
            atom_types.type_by_id_(i).radius = 1.2
            atom_types.type_by_id_(i).color = [c/255 for c in (255, 167, 26)]
        else:
            atom_types.type_by_id_(i).load_defaults()
