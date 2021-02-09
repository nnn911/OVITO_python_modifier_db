# OVITO Python script modifier database

Collection of python script modifiers for [OVITO Pro](https://www.ovito.org/). Each script is designed to be used on a data collection from the graphical user interface using the `python script modifier`. The OVITO version used for testing can be found in each individual script.

## FixParticleIdentifier.py
- Replaces the current `Particle Identifer` array with a new continuous one, starting at `init_val`. This can be necessary after particles were inserted or deleted.


## GenerateRandomSolution.py
- Replaces the current atomic configurations with a new random arrangement. The concentrations per species are given in the `conc` array (`sum conc == 1`).

## SelectSphere.py
- Select a spherical region of a given `radius` around a `center` point.
- `add_to_selection` toggle can be used to add to the current selection or create a new one.

## SelectCylinder.py
- Select a cylindrical region of a given `radius` from point `p1` to point `p2`.
- `add_to_selection` toggle can be used to add to the current selection or create a new one.