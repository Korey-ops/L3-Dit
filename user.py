import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random
import pyautogui
import sqlite3
from net import request

def user_frame(username):
    


    #connect to the database
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    #make the jobs table if it doesnt exist yet
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
    #main frame that holds everything
    frame = tk.Frame(root, background="#87D9F1")
    frame.pack( fill="both", expand=True)
    #blue bar across the top
    header_frame = tk.Frame(frame, background="#485BC9")
    header_frame.pack(anchor="center", fill="x")
    #frame for the form inputs
    user_frame = tk.Frame(frame, background="#87D9F1")
    user_frame.pack(anchor="center")


    #close the window and go back to the login page
    def log_out():
            root.destroy()
    
            
            from interface import login_page
            login_page()



    #title and log out button in the header
    title = tk.Label(header_frame, text="Mayfair admin", font=("arial", 28), background="#485BC9")
    title.pack(side="left", padx=20, pady=20)
    logout = tk.Button(header_frame, text="Log Out", command=log_out, anchor="e", background="#485BC9")
    logout.pack(side="right", padx=20)

    #name box filled in with the username
    name_label = tk.Label(user_frame, text="Name", font=("arial", 20), background="#87D9F1")
    name_label.pack()
    name_entry = ttk.Entry(user_frame, width=40)
    name_entry.insert(0, username)
    name_entry.pack(pady=10)

    #dropdown to pick the room
    location_label = tk.Label(user_frame, text="Location", font=("arial", 20), background="#87D9F1")
    location_label.pack()
    location_options = ["room1", "room2", "room3", "room4", "room5", "room6", "room7", "room8", "room9", "room10", "room11", "hall"]
    location_drop = ttk.Combobox(user_frame, values=location_options, state="readonly", width=37, background="#87D9F1")
    location_drop.set("choose an option")
    location_drop.pack(pady=10)

    #dropdown to pick the type of problem
    type_label = tk.Label(user_frame, text="type", width=40, font=("arial", 20), background="#87D9F1")
    type_label.pack()
    type_options = ["plumbing", "maintenance", "damage"]
    type_drop = ttk.Combobox(user_frame, values=type_options, state="readonly", width=37, background="#87D9F1")
    type_drop.set("choose an option")
    type_drop.pack(pady=10)



    current_rating = 0
    stars = []

    #fill in the stars up to the one clicked
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
    star_frame = tk.Frame(frame, background="#87D9F1")
    star_frame.pack(padx=30, anchor="center")


    for i in range (1, 6):
        label = tk.Label(star_frame, text="☆", foreground="gray", cursor="hand2", font=("Arial", 26))
        label.pack(side=tk.LEFT, padx=5)
        label.bind("<Button-1>", lambda e, v=i: rating(v))
        stars.append(label)
  

    #get the text from either an entry or a text box
    def get_text(widget):
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c")
        return widget.get()
 
    #clear an entry or a text box
    def clear_text(widget):
        if isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
        else:
            widget.delete(0, tk.END)
 
    #put text into an entry or a text box
    def insert_text(widget, text):
        if isinstance(widget, tk.Text):
            widget.insert("1.0", text)
        else:
            widget.insert(0, text)



    def clear_placeholder(event):
        #if the text matches the palceholder clear it
        #use a widget so both can be bound to the amse event
        widget = event.widget
        content = get_text(widget)

        if content == "please let us know whats wrong...":
            clear_text(widget)
            widget.config(foreground="black")

    #put the placeholder back if the box is left empty
    def restore_placeholder(event):
        widget = event.widget
        content = get_text(widget)

        if widget is expla_entry and content == "":
            insert_text(widget, "please let us know whats wrong...")
            widget.config(foreground="grey")


    
     
    #big text box to explain the problem
    expla_label = tk.Label(user_frame, text="What happened?", font=("arial", 20), background="#87D9F1")
    expla_label.pack(pady=10)
    expla_entry = tk.Text(user_frame, width=50, height=10)
    expla_entry.insert("1.0", "please let us know whats wrong...")
    expla_entry.pack(pady=10)
    




    #bind the placeholder functions to focus events
    name_entry.bind("<FocusIn>", clear_placeholder)
    name_entry.bind("<FocusOut>", restore_placeholder)
    expla_entry.bind("<FocusIn>", clear_placeholder)
    expla_entry.bind("<FocusOut>", restore_placeholder)
    
    
    #check the form then send the request to the server
    def add_request():
        #grab everything the user entered
        name = name_entry.get().strip()
        location = location_drop.get()
        typ = type_drop.get()
        urgency = "★" * current_rating + "☆" * (5 - current_rating)
        task = expla_entry.get("1.0", "end-1c").strip()

        #make sure every field is filled in
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if location == "choose an option":
            messagebox.showerror("Error", "Please select a location.")
            return
        if type == "choose an option":
            messagebox.showerror("Error", "Please select a type.")
            return
        if not task or task == "please let us know whats wrong...":
            messagebox.showerror("Error", "Please describe the issue.")
            return

        #send the job to the server
        try:
             response = request({"action": "submit_job", "name": name,
                                "location": location, "type": typ,
                                "urgency": urgency, "task": task})
        except Exception as e:
            messagebox.showerror("Connection error", str(e))
            return

        #reset the form if it worked
        if response.get("ok"):
            messagebox.showinfo("Success", "Your request has been submitted.")
            location_drop.set("choose an option")
            type_drop.set("choose an option")
            clear_text(expla_entry)
            insert_text(expla_entry, "please let us know whats wrong...")
            expla_entry.config(foreground="grey")
        else:
            messagebox.showerror("Error", response.get("error", "Submission failed"))

    #put the button below the stars so a new frame
    entry_frame = tk.Frame(frame, background="#87D9F1")
    entry_frame.pack(anchor="center")
    entry_button = tk.Button(entry_frame, text="enter request", command=add_request)
    entry_button.pack(side=tk.BOTTOM, pady=10)

    #show the emergency numbers
    def call_help():
        messagebox.showwarning("EMERGENCY","Call Admin, or emergency services 111 / 0272546342")
    
    emergency = tk.Button(entry_frame, text="EMERGENCY", command=call_help)
    emergency.pack(side=tk.BOTTOM, pady=10)


    root.mainloop()
if __name__ == "__main__":
    user_frame()