# OVITO Python script modifier database

Collection of python script modifiers for [OVITO Pro](https://www.ovito.org/). Each script is designed to be used on a data collection from the graphical user interface using the `python script modifier`. The OVITO version used for testing can be found in each individual script.

## Installation
To make these modifiers available from the 'Add modification...' dropdown menu the `*.py` files can be copied to `ovito-pro-root-dir/share/ovito/scripts/modifiers/`

## AddParticle.py
- Adds a single particle of type `symbol` (integer or string) at position `x`, `y`, `z` to the data collection.

## AddParticles.py
- Adds multiple particles defined by the particle type array `symbol` and the position arrays `x`, `y`, `z` to the data collection.

## FixParticleIdentifier.py
- Replaces the current `Particle Identifer` array with a new continuous one, starting at `init_val`. This can be necessary after particles were inserted or deleted.

## GenerateRandomSolution.py
- Replaces the current atomic configurations with a new random arrangement. The concentrations per species are given in the `conc` array (`sum conc == 1`).
- `only_selected` applies the modifier only to selected atoms.

## SelectSphere.py
- Select a spherical region of a given `radius` around a `center` point.
- `add_to_selection` toggle can be used to add to the current selection or create a new one.

## SelectCylinder.py
- Select a cylindrical region of a given `radius` from point `p1` to point `p2`.
- `add_to_selection` toggle can be used to add to the current selection or create a new one.