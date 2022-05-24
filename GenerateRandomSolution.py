# OVITO Pro 3.4.0

from ovito.data import *
import numpy as np


def _create_initial_conc_vec(length, conc):
    conc_vec = []
    for i, c in enumerate(conc):
        conc_vec += [i + 1] * int(length * c)
    return conc_vec


def _pad_conc_vec(conc_vec, length, conc):
    x_p = np.cumsum(conc)
    while len(conc_vec) < length:
        # conc_vec.append(np.sum(x_p < rng.random())+1)
        conc_vec.append(np.sum(x_p < np.random.random()) + 1)
    return conc_vec


def _calculate_concentration(data):
    pt, count = np.unique(data.particles["Particle Type"], return_counts=True)
    count = count / np.sum(count)
    print("New concentrations:")
    for p, c in zip(data.particles["Particle Type"].types, count):
        print(f"{p.name}: {c}")
    return pt, count


def modify(
    frame: int, data: DataCollection, conc=(0.5, 0.5), seed=123456, only_selected=False
):
    assert (not only_selected) | (
        "Selection" in data.particles.keys()
    ), "No selection defined!"
    assert np.isclose(np.sum(conc), 1), f"sum conc = {np.sum(conc)} != 1"

    np.random.seed = seed
    while len(conc) > len(data.particles["Particle Type"].types):
        new_id = len(data.particles["Particle Type"].types) + 1
        data.particles_["Particle Type_"].types.append(
            ParticleType(
                id=new_id,
                name=f"Type {new_id}",
                color=np.random.random(size=3),
            )
        )

    # new np syntax (currently not supported by ovito)
    # rng = np.random.default_rng(seed)
    np.random.seed = seed

    if only_selected:
        select = np.array(data.particles["Selection"])
        select = select.astype(int)

    length = data.particles.count if not only_selected else np.sum(select)
    conc_vec = _create_initial_conc_vec(length, conc)
    conc_vec = _pad_conc_vec(conc_vec, length, conc)

    conc_vec = np.array(conc_vec)
    np.random.shuffle(conc_vec)
    # rng.shuffle(conc_vec)

    if only_selected:
        data.particles_["Particle Type_"][np.where(select == 1)[0]] = conc_vec
    else:
        data.particles_["Particle Type_"][...] = conc_vec
    _ = _calculate_concentration(data)
