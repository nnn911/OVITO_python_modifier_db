from ovito.data import *
from numpy.random import default_rng


def modify(
    frame: int,
    data: DataCollection,
    mode: str = "uniform",
    amp: float = 1e-6,
    seed: int = None,
):
    rng = default_rng(seed)
    if mode.lower() == "uniform":
        jiggle = 2 * amp * rng.random(size=(data.particles.count, 3)) - amp
    elif mode.lower() == "normal":
        jiggle = rng.normal(loc=0, scale=amp, size=(data.particles.count, 3))
    else:
        raise ValueError(f"{mode = } unkown!")
    data.particles_["Position_"][...] += jiggle
