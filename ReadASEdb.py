from ovito.data import *
from ovito.vis import *

from numpy import unique
import os
import ase.db


class ase_db_helper:
    def __init__(self, path=None):
        self.path = ""
        if path:
            self.load_db(path)

    def load_db(self, path):
        assert os.path.isfile(path), f"{path} does not exist!"
        if path != self.path:
            self.path = path
            self.db = ase.db.connect(path)

    def select_frame(self, frame):
        ret = list(self.db.select(frame))
        if len(ret) != 1:
            raise IndexError("Row not in database")
        return ret[0].toatoms()


g_db = ase_db_helper()


def create(frame: int, data: DataCollection, db_row=1, path=""):
    global g_db
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} not found!")

    g_db.load_db(path)
    atoms = g_db.select_frame(db_row)

    del data.objects[:]

    elements = unique(atoms.get_chemical_symbols())

    data.objects.append(Particles())
    data.particles_.count = atoms.get_number_of_atoms()
    data.particles_.create_property("Position", data=atoms.positions)

    type_property = data.particles_.create_property("Particle Type")
    for e, element in enumerate(elements):
        type_property.types.append(ParticleType(id=e + 1, name=element))
        type_property.type_by_name(element).load_defaults()

    type_property[...] = [
        type_property.type_by_name(e).id for e in atoms.get_chemical_symbols()
    ]

    data.objects.append(
        SimulationCell(pbc=atoms.pbc, vis=SimulationCellVis(line_width=0.03))
    )
    data.cell_[:, :3] = atoms.cell.T
    data.cell_[:, 3] = [0, 0, 0]
    print("Success!")
