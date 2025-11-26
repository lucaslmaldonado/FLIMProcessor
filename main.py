###
# Software developed by Lucas Lopes Maldonado
# The intent of this software is to analyze FLIM images, returning parameters such as the Metabolic Index and FLIR
# for selected regions on the images.
#
###

from controller import Controller
from model import Model
from view import View
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()