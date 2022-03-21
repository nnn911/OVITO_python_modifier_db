# OVITO Python script modifier database

Collection of python script modifiers for [OVITO Pro](https://www.ovito.org/). Each script is designed to be used on a data collection from the graphical user interface using the `python script modifier`. The OVITO version used for testing can be found in each individual script.

## Installation
To make these modifiers available from the 'Add modification...' dropdown menu the `*.py` files can be copied to `ovito-pro-root-dir/share/ovito/scripts/modifiers/`

# Modifiers
## AddParticle.py
- Adds a single particle of type `symbol` (integer or string) at position `x`, `y`, `z` to the data collection.

## AddParticles.py
- Adds multiple particles defined by the particle type array `symbol` and the position arrays `x`, `y`, `z` to the data collection.

## ApplyDefaultParticleTypes.py
- Reads the species names, e.g. Cu, from the `types` property and applies the corresponding default settings stored in OVITO.
## FixParticleIdentifier.py
- Replaces the current `Particle Identifer` array with a new continuous one, starting at `init_val`. This can be necessary after particles were inserted or deleted.

## GenerateRandomSolution.py
- Replaces the current atomic configurations with a new random arrangement. The concentrations per species are given in the `conc` array (`sum conc == 1`).
- `only_selected` applies the modifier only to selected atoms.

## JiggleAtoms.py
- Randomly displaces all atoms.
- `mode` can be either "uniform" or "normal". Depending on the mode, random displacements are either drawn from a uniform or normal distribution.
- `amp` gives the displacement magnitude (mode: uniform) or standard deviation (mode: normal)
- `seed` sets the starting value of the random number generator.

## SelectSphere.py
- Select a spherical region of a given `radius` around a `center` point.
- `add_to_selection` toggle can be used to add to the current selection or create a new one.

## SelectCylinder.py
- Select a cylindrical region of a given `radius` from point `p1` to point `p2`.
- `add_to_selection` toggle can be used to add to the current selection or create a new one.

# File Readers

## ReadASEdb.py
- Read an ASE database into the timeline

## ReadMol2file.py
- Read a mol2 file into the timeline