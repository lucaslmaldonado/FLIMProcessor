import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from polygon_selector import MyPolygonSelector
from matplotlib.patches import Polygon

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("FLIMProcessor")

        #try:
        #    self.root.state('zoomed')  # Works on Windows
        #except tk.TclError:
        #    # Fallback for Linux/Mac
        #    screen_width = self.root.winfo_screenwidth()
        #    screen_height = self.root.winfo_screenheight()
        #    self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.fig, self.ax_img = plt.subplots(1, 1, figsize=(5, 5))
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=1)
        self.ax_img.set_xticks([])
        self.ax_img.set_yticks([])

        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add region button
        self.new_region_button = ttk.Button(self.root, text="New Region", command=self.controller.new_region, bootstyle=PRIMARY)
        self.new_region_button.pack(side=tk.LEFT, fill=tk.X, padx=5)
        # Add analyze button
        self.analyze_button = ttk.Button(self.root, text="Process Region", command=self.controller.process_region, bootstyle=PRIMARY)
        self.analyze_button.pack(side=tk.LEFT, fill=tk.X, padx=5)
        # Add save button
        self.save_button = ttk.Button(self.root, text='Save', command=self.controller.save_data, bootstyle=SUCCESS)
        self.save_button.pack(side=tk.LEFT, fill=tk.X, padx=5)

        # Menu bar
        self.menu_bar = ttk.Menu(self.root)
        # File cascade
        self.file_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Image", command = self.controller.load_image)
        self.file_menu.add_command(label="Exit", command = self.controller.quit_app)
        # Settings cascade
        self.settings_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.root.config(menu=self.menu_bar)

        self.polygon_interactor = None

    
    def show_image(self, image):
        self.ax_img.clear()
        self.ax_img.imshow(image, origin='upper')
        self.ax_img.set_title("")
        self.ax_img.set_axis_off()
        self.canvas.draw_idle()

    def update_image(self, image, regions):
        self.ax_img.clear()
        self.ax_img.imshow(image, origin='upper')
        self.ax_img.set_title("")
        self.ax_img.set_axis_off()
        self.canvas.draw_idle()
        for verts in regions:
            poly = Polygon(verts, closed=True,
                    facecolor='red', edgecolor='red', alpha=0.5)
            self.ax_img.add_patch(poly)

    def set_polygon_selector(self):#, onselect_callback):
        if self.polygon_interactor is not None:
            self.polygon_interactor.disconnect()
        self.polygon_interactor = MyPolygonSelector(self.ax_img)
        self.canvas.draw_idle()

    def get_coords(self):
        return self.polygon_interactor.get_coords()
    
    def get_figure(self):
        return self.fig
