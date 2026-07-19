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

    type_options = ["plumbing", "maintenance", "damage"]
    type_drop = ttk.Combobox(user_frame, values=type_options, state="readonly")
    type_drop.set("choose an option")
    type_drop.pack(pady=10)



    current_rating = 0
    stars = []

    def rating(val):
        global current_rating
        current_rating = val
        for i, star in enumerate(stars):
            if i < val:
                star.config(text="★", foreground="gold")
            else:
                star.config(text="☆", foreground="gray")
        print(f"Selected rating: {val}")

    #create 5 stars
    star_frame = tk.Frame(root)
    star_frame.pack(padx=30)


    for i in range (1, 6):
        label = tk.Label(star_frame, text="☆", foreground="gray", cursor="hand2")
        label.pack(side=tk.LEFT, padx=5)
        label.bind("<Button-1>", lambda e, v=i: rating(v))
        stars.append(label)
  

    def Clear_placeholder(event):
        #if the text matches the palceholder clear it
        if name_entry.get() == "enter your name...":
            name_entry.delete(0, tk.END)
            name_entry.config(foreground="black") #change text colour
        if expla_entry.get() == "please let us know whats wrong...":
            expla_entry.delete(0, tk.END)
            expla_entry.config(foreground="black")

    def restore_placeholder(event):
        if name_entry.get() == "":
            name_entry.insert(0, "enter your name...")
            name_entry.config(foreground="grey")
        if expla_entry.get() == "":
            expla_entry.insert(0, "please let us know whats wrong...")
            expla_entry.config(foreground="grey")





    Name = tk.Label(user_frame, text="Name", font=("arial", 12))
    Name.pack(pady=10)

    name_entry = ttk.Entry(user_frame, width=40)
    name_entry.insert(0, "enter your name...")
    name_entry.config(foreground="grey")
    name_entry.pack(pady=10)


    
     
    expla_label = tk.Label(user_frame, text="input actual taks")
    expla_label.pack(pady=10)
    expla_entry = ttk.Entry(user_frame, )
    expla_entry.pack(pady=10)
    




    name_entry.bind("<FocusIn>", Clear_placeholder)
    name_entry.bind("<FocusOut>", restore_placeholder)
    expla_entry.bind("<FocusIn>", Clear_placeholder)
    expla_entry.bind("<FocusOut>", restore_placeholder)


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