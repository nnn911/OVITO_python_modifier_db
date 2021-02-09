# OVITO Pro 3.4.0

from ovito.data import *
from ovito.modifiers import ExpressionSelectionModifier


def modify(frame: int, data: DataCollection, radius=2.0, center=(0.0, 0.0, 0.0), add_to_selection=True):
    x1, y1, z1 = center

    eq = f'((Position.X-{x1})^2+(Position.Y-{y1})^2+(Position.Z-{z1})^2'

    if add_to_selection and 'Selection' in data.particles.keys():
        expr = f'(Selection==1) || {eq}<={radius**2})'
    else:
        expr = f'{eq}<={radius**2})'
    data.apply(ExpressionSelectionModifier(expression=expr))
