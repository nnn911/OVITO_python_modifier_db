from multiprocessing.sharedctypes import Value
from ovito.data import NearestNeighborFinder, DataCollection
from numpy import zeros, cumsum, array


def modify(
    frame: int,
    data: DataCollection,
    num_neighors=[12, 8],
    only_selected=False,
    use_particle_identifier=True,
):
    if isinstance(num_neighors, int):
        num_neighors = [num_neighors]
    elif not isinstance(num_neighors, list):
        raise ValueError(
            "num_neighors variable needs to be a list of atoms per neighbor shell"
        )
    if sum(num_neighors) > 30:
        raise ValueError("The total number of neighbors has to be less than 30")
    if use_particle_identifier and ("Particle Identifier" not in data.particles.keys()):
        raise ValueError("Particle Identifier not found in DataCollection")
    if only_selected and ("Selection" not in data.particles.keys()):
        raise ValueError("No Selection defined")

    finder = NearestNeighborFinder(sum(num_neighors), data)
    neighbor_list = zeros((data.particles.count, sum(num_neighors)), dtype=int)
    part_ident = array(data.particles["Particle Identifier"])
    if only_selected:
        selection = array(data.particles["Selection"])
    for index in range(data.particles.count):
        if only_selected and (not selection[index]):
            continue
        for i, neigh in enumerate(finder.find(index)):
            if use_particle_identifier:
                neigh = part_ident[neigh.index]
            else:
                neigh = neigh.index
            neighbor_list[index, i] = neigh
        yield index / data.particles.count

    csum = [0] + list(cumsum(num_neighors))
    for i, _ in enumerate(csum):
        if i == 0:
            continue
        data.particles_.create_property(
            f"{i} neighbor shell", data=(neighbor_list[:, csum[i - 1] : csum[i]])
        )
