from ovito.data import *
from ovito.io.ase import ase_to_ovito
from ase.atoms import Atoms
from ovito.pipeline import StaticSource
from ovito.modifiers import CombineDatasetsModifier


def modify(frame: int, data: DataCollection, x=[0.0, 1.0], y=[0.0, 1.0], z=[0.0, 1.0], symbol=['H', 'C']):
    if (len(x) != len(y)) or (len(x) != len(z)) or (len(x) != len(symbol)):
        print('Input arrays not of equal length! Skipping ...')
    else:
        atoms = Atoms(symbol,
                      positions=[[float(X), float(Y), float(Z)] for X, Y, Z in zip(x, y, z)])
        new_data = ase_to_ovito(atoms)

        modifier = CombineDatasetsModifier()
        modifier.source = StaticSource(data=new_data)
        data.apply(modifier)
