from skimage import io
import numpy as np
from pathlib import Path as file_Path
from matplotlib.path import Path
import pandas as pd
from tkinter import filedialog

class Model:
    def __init__(self):
        self.regions = []
        self.image = None

    def load_image(self, path):
        img = io.imread(path)
        if img.ndim == 3:
            if img.shape[2] == 4:
                img = img[..., :3]
        self.image = img
        self.load_files(path)
        return self.image
    
    def clear(self):
        self.regions = []
        self.image = None
    
    def load_files(self, path):
        filepath = file_Path(path)
        # Extract folder and base prefix
        self.folder = filepath.parent
        stem = filepath.stem

        # Remove termination to get the common base prefix
        if stem.endswith('FAD_intensity_image'):
            base_prefix = stem[:-20]
        elif stem.endswith('FAD_color_Image'):
            base_prefix = stem[:-16]
        elif stem.endswith('NADH_intensity_image'):
            base_prefix = stem[:-21]
        elif stem.endswith('NADH_color_Image'):
           base_prefix = stem[:-17]    
        else:
            raise ValueError("Filename does not follow expected pattern *_NADH_intensity_image.tif or *_NADH_color_Image.tif.")
        
        # Construct full paths to the other files
        NADH_t1_path = self.folder / f"{base_prefix}_NADH_t1.asc"
        NADH_a1_path = self.folder / f"{base_prefix}_NADH_a1.asc"
        NADH_t2_path = self.folder / f"{base_prefix}_NADH_t2.asc"
        NADH_a2_path = self.folder / f"{base_prefix}_NADH_a2.asc"
        FAD_t1_path  = self.folder / f"{base_prefix}_FAD_t1.asc"
        FAD_a1_path  = self.folder / f"{base_prefix}_FAD_a1.asc"
        FAD_t2_path  = self.folder / f"{base_prefix}_FAD_t2.asc"
        FAD_a2_path  = self.folder / f"{base_prefix}_FAD_a2.asc"

        self.NADH_t1 = np.loadtxt(NADH_t1_path)[::-1,::]
        self.NADH_t2 = np.loadtxt(NADH_t2_path)[::-1,::]
        self.NADH_a1 = np.loadtxt(NADH_a1_path)[::-1,::]
        self.NADH_a2 = np.loadtxt(NADH_a2_path)[::-1,::]
        self.FAD_t1 = np.loadtxt(FAD_t1_path)[::-1,::]
        self.FAD_t2 = np.loadtxt(FAD_t2_path)[::-1,::]
        self.FAD_a1 = np.loadtxt(FAD_a1_path)[::-1,::]
        self.FAD_a2 = np.loadtxt(FAD_a2_path)[::-1,::]
        self.NADH_a1r = self.NADH_a1 / (self.NADH_a1 + self.NADH_a2)
        self.NADH_a2r = self.NADH_a2 / (self.NADH_a1 + self.NADH_a2)
        self.FAD_a1r = self.FAD_a1 / (self.FAD_a1 + self.FAD_a2)
        self.FAD_a2r = self.FAD_a1 / (self.FAD_a1 + self.FAD_a2)
        self.NADH_Int = self.NADH_a1 + self.NADH_a2
        self.FAD_Int = self.FAD_a1 + self.FAD_a2

    def process_region(self, coords):
        self.create_mask(coords)
        self.regions.append(coords)

        self.processed_data = {"x": [], "y": [], 
                  "NADH_t1": [], "NADH_t2": [], "NADH_a1": [], "NADH_a2": [], "NADH_a1[%]": [], "NADH_a2[%]": [], "NADH_tm": [],
                  "FAD_t1": [], "FAD_t2": [], "FAD_a1": [], "FAD_a2": [], "FAD_a1[%]": [], "FAD_a2[%]": [],"FAD_tm": [],
                  "NADH a1 / NADH a2": [], "NADH a2 / FAD a1": [], "NADH_Int": [], "FAD_Int": []}
        for x,y in self.pixel_indices:
            self.processed_data["x"].append(x)
            self.processed_data["y"].append(y)
            self.processed_data["NADH_t1"].append(self.NADH_t1[x,y])
            self.processed_data["NADH_t2"].append(self.NADH_t2[x,y])
            self.processed_data["NADH_a1"].append(self.NADH_a1[x,y])
            self.processed_data["NADH_a2"].append(self.NADH_a2[x,y])
            self.processed_data["NADH_a1[%]"].append(self.NADH_a1r[x,y])
            self.processed_data["NADH_a2[%]"].append(self.NADH_a2r[x,y])
            self.processed_data["FAD_t1"].append(self.FAD_t1[x,y])
            self.processed_data["FAD_t2"].append(self.FAD_t2[x,y])
            self.processed_data["FAD_a1"].append(self.FAD_a1[x,y])
            self.processed_data["FAD_a2"].append(self.FAD_a2[x,y])
            self.processed_data["FAD_a1[%]"].append(self.FAD_a1r[x,y])
            self.processed_data["FAD_a2[%]"].append(self.FAD_a2r[x,y])
            NAD_tm = (self.NADH_a1[x,y]*self.NADH_t1[x,y] + self.NADH_a2[x,y]*self.NADH_t2[x,y])/(self.NADH_a1[x,y]+self.NADH_a2[x,y])
            FAD_tm = (self.FAD_a1[x,y]*self.FAD_t1[x,y] + self.FAD_a2[x,y]*self.FAD_t2[x,y])/(self.FAD_a1[x,y]+self.FAD_a2[x,y])
            self.processed_data["NADH_tm"].append(NAD_tm)
            self.processed_data["FAD_tm"].append(FAD_tm)
            self.processed_data["NADH a1 / NADH a2"].append(self.NADH_a1r[x,y]/self.NADH_a2r[x,y])
            self.processed_data["NADH a2 / FAD a1"].append(self.NADH_a2r[x,y]/self.FAD_a1r[x,y])
            self.processed_data["NADH_Int"].append(self.NADH_Int[x,y])
            self.processed_data["FAD_Int"].append(self.FAD_Int[x,y])
    
    def create_mask(self, coords):
        ny, nx = self.image.shape[:2]
        y, x = np.mgrid[0:ny, 0:nx]
        points = np.vstack((x.ravel(), y.ravel())).T
        path = Path(coords)
        self.mask = path.contains_points(points).reshape((ny, nx))
        self.pixel_indices = np.argwhere(self.mask)

    def save_data(self, figure):
        df = pd.DataFrame(self.processed_data)

        save_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",  # or .png, .csv etc.
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                    title="Save Region As"
                )
        if save_path:
            df.to_excel(save_path, index=False)
            figure.savefig(save_path.split(".")[0]+".png")
            print(f"Data saved to {save_path}")
        else:
            print("Save canceled.")

    def get_regions(self):
        return self.regions
    