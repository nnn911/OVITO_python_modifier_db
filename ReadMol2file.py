from ovito.data import *
from ovito.vis import *
import os
import re
import numpy as np


class myAtoms:
    def __init__(self):
        self.ids = []
        self.ptypes = []
        self.hybrid = []
        self.pos = [[], [], []]

    def add_line(self, line):
        line = line.split()
        self.ids.append(int(line[0]))
        self.ptypes.append(self.split_ptype(line[1]))
        self.hybrid.append(line[5])
        for i in range(3):
            self.pos[i].append(float(line[2 + i]))

    def split_ptype(self, ptype):
        return re.split("[0-9]", ptype, 1)[0]

    def get_elements(self):
        return np.unique(self.ptypes)

    def get_shifted_positions(self):
        pos = np.array(self.pos)
        pos = pos.T - np.mean(pos, axis=1)
        return pos


class myBonds:
    def __init__(self):
        self.ids = []
        self.topo = [[], []]
        self.btypes = []

    def add_line(self, line):
        line = line.split()
        self.ids.append(int(line[0]))
        self.btypes.append(self.remap_bond_types(line[3]))
        for i in range(2):
            self.topo[i].append(int(line[1 + i]))

    def get_bonds(self):
        return np.transpose(self.topo) - 1

    def remap_bond_types(self, btype):
        remap = {"am": 4, "ar": 5, "du": 6, "un": 7, "nc": 8}
        if btype in remap:
            return remap[btype]
        return int(btype)


class mol2_helper:
    def __init__(self, path):
        assert os.path.isfile(path)
        self.path = path

    def read_frame(self, mol2file, target_frame):
        assert target_frame >= 0
        atoms = myAtoms()
        bonds = myBonds()

        flags = self.init_flags(target_frame)
        for line in mol2file:
            flags = self.decide_process_frame(line, flags)
            if flags["done"]:
                return atoms, bonds
            if not flags["to_process"]:
                continue

            flags = self.decide_block(line, flags)
            if flags["just_updated"]:
                continue
            if flags["block"] == "ATOM":
                atoms.add_line(line)
            elif flags["block"] == "BOND":
                bonds.add_line(line)
        raise IndexError(
            f'target_frame: {target_frame} not in file! {flags["current_frame"]-1} frames found!'
        )

    def init_flags(self, target_frame):
        flags = {
            "current_frame": 0,
            "target_frame": target_frame,
            "to_process": False,
            "done": False,
            "block": "",
            "just_updated": False,
        }
        return flags

    def decide_process_frame(self, line, flags):
        if line.startswith(r"@<TRIPOS>MOLECULE") and (
            flags["current_frame"] == flags["target_frame"]
        ):
            flags["to_process"] = True
            flags["current_frame"] += 1
        elif line.startswith(r"@<TRIPOS>MOLECULE") and (
            flags["current_frame"] < flags["target_frame"]
        ):
            flags["current_frame"] += 1
        elif line.startswith(r"@<TRIPOS>MOLECULE") and (
            flags["current_frame"] > flags["target_frame"]
        ):
            flags["done"] = True
        return flags

    def decide_block(self, line, flags):
        if flags["just_updated"]:
            flags["just_updated"] = False
        if line.startswith(r"@<TRIPOS>"):
            flags["block"] = line.strip()[len("@<TRIPOS>") :]
            flags["just_updated"] = True
        return flags

    def get_frame(self, frame):
        with open(self.path, "r") as mol2file:
            return self.read_frame(mol2file, frame)


def create(frame: int, data: DataCollection, path="", select_frame=0):
    del data.objects[:]

    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} not found!")

    m2h = mol2_helper(path)
    atoms, bonds = m2h.get_frame(select_frame)

    data.objects.append(Particles())
    data.particles_.count = len(atoms.ids)
    data.particles_.create_property("Position", data=atoms.get_shifted_positions())

    type_property = data.particles_.create_property("Particle Type")
    for e, element in enumerate(atoms.get_elements()):
        type_property.types.append(ParticleType(id=e + 1, name=element))
        type_property.type_by_name(element).load_defaults()
    type_property[...] = [type_property.type_by_name(e).id for e in atoms.ptypes]

    assert all([(b - a) == 1 for a, b in zip(atoms.ids[:-1], atoms.ids[1:])])
    data.particles_.bonds = Bonds(vis=BondsVis(width=0.6))
    data.particles_.bonds_.count = len(bonds.topo[0])
    data.particles_.bonds_.create_property("Topology", data=bonds.get_bonds())
    data.particles_.bonds_.create_property("bType", data=bonds.btypes)
