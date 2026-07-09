import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random
import pyautogui


#initialise main window
size = pyautogui.resolution()
root = tk.Tk()
root.title("work forum")
root.geometry("1920x1080")

def user_Frame():



    root = tk.Tk()
    frame = tk.Frame(root)
    frame.place( relx=0.5, rely=0.5, anchor="center")

    user_frame = tk.Frame(root)
    user_frame.pack()



    location_options = ["room1", "room2", "room3", "room4", "room5", "room6", "room7", "room8", "room9", "room10", "room11", "hall"]
    location_drop = ttk.Combobox(user_frame, values=location_options, state="readonly")
    location_drop.set("choose an option")
    location_drop.pack(pady=10)





user_Frame




root.mainloop()


