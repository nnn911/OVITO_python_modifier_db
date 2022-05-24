from ovito.data import *


def modify(frame: int, data: DataCollection, names=[]):
    atom_types = data.particles_.particle_types_
    while len(names) > len(data.particles["Particle Type"].types):
        new_id = len(data.particles["Particle Type"].types) + 1
        data.particles_["Particle Type_"].types.append(
            ParticleType(
                id=new_id,
                name=f"Type {new_id}",
                color=(0.8, 0.8, 0.8),
            )
        )
    for i in range(1, len(names) + 1):
        atom_types.type_by_id_(i).name = names[i - 1]
        if names[i - 1] == "Mn":
            atom_types.type_by_id_(i).radius = 1.2
            atom_types.type_by_id_(i).color = [c / 255 for c in (255, 167, 26)]
            atom_types.type_by_id_(i).mass = 54.938044
        else:
            atom_types.type_by_id_(i).load_defaults()
