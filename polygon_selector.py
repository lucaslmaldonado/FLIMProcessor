import numpy as np
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path

class MyPolygonSelector:
    def __init__(self, ax):
        self.ax = ax
        self.selector = PolygonSelector(ax, self.onselect, props=dict(color='red', linestyle='-', linewidth=2, alpha=0.8), useblit=True)
        self.coords = None
        self.mask = None
        self.pixel_indices = None
        self.done = False
        print("Draw a polygon and close it.")

    def onselect(self, verts):
        self.coords = np.array(verts)
        self.done = True

    def get_coords(self):
        return self.coords

    def disconnect(self):
        self.selector = None
