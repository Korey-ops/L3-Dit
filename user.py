import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random
import pyautogui

def user_frame(content):

    #initialise main window
    root = tk.Tk()
    root.title("work forum")
    root.geometry(pyautogui.size())

    frame = tk.Frame(root)
    frame.place( relx=0.5, rely=0.5, anchor="center")

    user_frame = tk.Frame(root)
    user_frame.pack


    root.mainloop()


user_frame().pack()