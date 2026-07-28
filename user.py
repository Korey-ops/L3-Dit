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
                CREATE TABLE IF NOT EXISTS jobs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT,
                type TEXT,
                urgency TEXT,
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
        nonlocal current_rating
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
  

    def get_text(widget):
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c")
        return widget.get()
 
    def clear_text(widget):
        if isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
        else:
            widget.delete(0, tk.END)
 
    def insert_text(widget, text):
        if isinstance(widget, tk.Text):
            widget.insert("1.0", text)
        else:
            widget.insert(0, text)



    def Clear_placeholder(event):
        #if the text matches the palceholder clear it
        #use a widget so both can be bound to the amse event
        widget = event.widget
        content = get_text(widget)

        if content == "enter your name...":
            clear_text(widget)
            widget.config(foreground="black") #change text colour

        elif content == "please let us know whats wrong...":
            clear_text(widget)
            widget.config(foreground="black")

    def restore_placeholder(event):
        widget = event.widget
        content = get_text(widget)

        if widget is name_entry and content == "":
            insert_text(widget, "enter your name...")
            widget.config(foreground="grey")

        elif widget is expla_entry and content == "":
            insert_text(widget, "please let us know whats wrong...")
            widget.config(foreground="grey")





    Name = tk.Label(user_frame, text="Name", font=("arial", 12))
    Name.pack(pady=10)

    name_entry = ttk.Entry(user_frame, width=40)
    name_entry.insert(0, "enter your name...")
    name_entry.config(foreground="grey")
    name_entry.pack(pady=10)


    
     
    expla_label = tk.Label(user_frame, text="input actual taks")
    expla_label.pack(pady=10)
    expla_entry = tk.Text(user_frame, width=150, height=20)
    expla_entry.insert("1.0", "please let us know whats wrong...")
    expla_entry.pack(pady=10)
    




    name_entry.bind("<FocusIn>", Clear_placeholder)
    name_entry.bind("<FocusOut>", restore_placeholder)
    expla_entry.bind("<FocusIn>", Clear_placeholder)
    expla_entry.bind("<FocusOut>", restore_placeholder)
    
    
    def add_request():
        name = name_entry.get()
        location = location_drop.get()
        typ = type_drop.get()
        urgency = "★" * current_rating + "☆" * (5 - current_rating)
        task = expla_entry.get("1.0", "end-1c")

        request_conn = sqlite3.connect("jobs.db")
        request_cursor = request_conn.cursor()
        request_cursor.execute("""
                        INSERT INTO jobs
                        (name, location, type, urgency, task)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (name, location, typ, urgency, task)
                        )
        request_conn.commit()
        request_conn.close()
        messagebox.showinfo("Success", "Your request has been submitted.")

    entry_button = tk.Button(user_frame, text="enter request", command=add_request)
    entry_button.pack(side=tk.BOTTOM, pady=10)


    root.mainloop()





user_frame()