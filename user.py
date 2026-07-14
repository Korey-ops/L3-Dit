import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random
import pyautogui
import sqlite3


def user_frame():




    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS task(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL)""")
    conn.commit()


    #initialise main window
    size = pyautogui.resolution()
    root = tk.Tk()
    root.title("work forum")
    root.geometry("1920x1080")
    frame = tk.Frame(root)
    frame.place( relx=0.5, rely=0.5, anchor="center")

    user_frame = tk.Frame(root)
    user_frame.pack()



    location_options = ["room1", "room2", "room3", "room4", "room5", "room6", "room7", "room8", "room9", "room10", "room11", "hall"]
    location_drop = ttk.Combobox(user_frame, values=location_options, state="readonly")
    location_drop.set("choose an option")
    location_drop.pack(pady=10)

    location_options = ["room1", "room2", "room3", "room4", "room5", "room6", "room7", "room8", "room9", "room10", "room11", "hall"]
    location_drop = ttk.Combobox(user_frame, values=location_options, state="readonly")
    location_drop.set("choose an option")
    location_drop.pack(pady=10)


    Name = tk.Label(user_frame, text="Name", font=("arial", 12))
    Name.pack(pady=10)

    entry_button = tk.Button(user_frame, text="enter request")
    entry_button.pack(side=tk.BOTTOM, pady=10)


    def add_request():
        name = entry_button.get()
        conn = sqlite3.connect("jobs.db")
        cursor.execute("INSERT INTO people (name) \ VALUES (?), (name,)")
        conn.commit()
        conn.close()
     







    root.mainloop()





user_frame()