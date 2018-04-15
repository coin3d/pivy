from pivy import coin
from .mesh import simple_quad_mesh
import numpy as np

def plot(foo, x, y):
    """x, y are tuples of 3 values: xmin, xmax, xnum"""
    np_foo = np.vectorize(foo)
    x_space = np.linspace(*x)
    y_space = np.linspace(*y)
    xx, yy = np.meshgrid(x_space, y_space)
    xx = xx.flatten()
    yy = yy.flatten()
    zz = np_foo(xx, yy)
    num_x = x[-1]
    num_y = y[-1]
    points = np.array([xx, yy, zz]).T
    scale = coin.SoScale()
    scale.scaleFactor.setValue(1, 1, abs(x[1] - x[0]) / abs(max(zz) - min(zz)))
    return [scale, simple_quad_mesh(points, num_x, num_y)]
