# OVITO Pro 3.4.0

from ovito.data import *
from ovito.modifiers import ExpressionSelectionModifier


def modify(frame: int, data: DataCollection, radius=2.0, p1=(0.0, 0.0, 0.0),
           p2=(0.0, 0.0, 0.0), add_to_selection=True):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    xn, yn, zn = x2-x1, y2-y1, z2-z1

    denom = (x2-x1)**2+(y2-y1)**2+(z2-z1)**2
    enum1 = f'((Position.Y-{y1})*(Position.Z-{z2})-(Position.Z-{z1})*(Position.Y-{y2}))^2'
    enum2 = f'((Position.Z-{z1})*(Position.X-{x2})-(Position.X-{x1})*(Position.Z-{z2}))^2'
    enum3 = f'((Position.X-{x1})*(Position.Y-{y2})-(Position.Y-{y1})*(Position.X-{x2}))^2'

    cylinder = f'({enum1}+{enum2}+{enum3})/({denom})<={3*radius**2}'
    base = f'{xn}*(Position.X-{x1})+{yn}*(Position.Y-{y1})+{zn}*(Position.Z-{z1}) > 0'
    top = f'{xn}*(Position.X-{x2})+{yn}*(Position.Y-{y2})+{zn}*(Position.Z-{z2}) < 0'

    if add_to_selection and 'Selection' in data.particles.keys():
        expr = f'(Selection==1) || ({cylinder} && {base} && {top})'
    else:
        expr = f'{cylinder} && {base} && {top}'
    data.apply(ExpressionSelectionModifier(expression=expr))
