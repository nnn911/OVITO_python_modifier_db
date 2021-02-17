from ovito.data import *
from ovito.io.ase import ase_to_ovito
from ase.atoms import Atoms
from ovito.pipeline import StaticSource
from ovito.modifiers import CombineDatasetsModifier


def modify(frame: int, data: DataCollection, x=0.0, y=0.0, z=0.0, symbol='H'):
    atoms = Atoms(symbol, positions=[(x, y, z)])
    new_data = ase_to_ovito(atoms)

    modifier = CombineDatasetsModifier()
    modifier.source = StaticSource(data=new_data)
    data.apply(modifier)
