# OVITO Pro 3.4.0

from ovito.data import *
from ovito.modifiers import ExpressionSelectionModifier


def modify(frame: int, data: DataCollection, radius=2.0, p1=(0.0, 0.0, 0.0),
           p2=(0.0, 0.0, 0.0), add_to_selection=True):
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    denom = (x2-x1)**2+(y2-y1)**2+(z2-z1)**2
    enum1 = f'((Position.Y-{y1})*(Position.Z-{z2})-(Position.Z-{z1})*(Position.Y-{y2}))^2'
    enum2 = f'((Position.Z-{z1})*(Position.X-{x2})-(Position.X-{x1})*(Position.Z-{z2}))^2'
    enum3 = f'((Position.X-{x1})*(Position.Y-{y2})-(Position.Y-{y1})*(Position.X-{x2}))^2'

    if add_to_selection and 'Selection' in data.particles.keys():
        expr = f'(Selection==1) || (({enum1})/({denom})+({enum2})/({denom})+({enum3})/({denom})<={radius**2})'
    else:
        expr = f'({enum1})/({denom})+({enum2})/({denom})+({enum3})/({denom})<={radius**2}'
    data.apply(ExpressionSelectionModifier(expression=expr))
