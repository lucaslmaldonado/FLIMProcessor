from model import Model
from view import View
from tkinter import filedialog
import matplotlib.pyplot as plt


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)
        self.root = root

        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def load_image(self):
        self.model.clear()
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.tif;*.tiff;*.bmp;*.jpeg")]
        )
        if not file_path:
            return
        self.image = self.model.load_image(file_path)
        self.view.show_image(self.image)

    def new_region(self):
        self.view.set_polygon_selector()
    
    def process_region(self):
        coords = self.view.get_coords()
        self.model.process_region(coords)
        regions = self.model.get_regions()
        self.view.update_image(self.image, regions)

    def save_data(self):
        figure = self.view.get_figure()
        self.model.save_data(figure)
    
    def quit_app(self):
        plt.close('all')
        self.root.destroy()