import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random
from user import user_frame
from admin import admin_pannel
import json
from net import request


#check the login details with the server then open the right page
def login():
    global username, password
    username = username_entry.get().strip()
    password = password_entry.get()

    #make sure both boxes are filled in
    if username and password:
        try:
            response = request({"action": "login",
                                "username": username,
                                "password": password})
            #close the login window and open the admin or user page
            if response.get("ok"):
                root.destroy()
                if response.get("is_admin"):
                    admin_pannel()
                else:
                    user_frame(username)
            else:
                messagebox.showerror("login", "Failed")
        except Exception as e:
            messagebox.showerror("Connection error", str(e))
    else:
        messagebox.showwarning("Missing Fields", "Please enter both Username and Passwords")

#build and show the login window
def login_page():

    global root, username_entry, password_entry


    #initialise main window
    root = tk.Tk()
    root.title("work forum")
    root.geometry("1920x1080")

    #frame in the middle of the window
    frame = tk.Frame(root)
    frame.place( relx=0.5, rely=0.5, anchor="center")

    #load the background image
    img_file = Image.open("bg.png")
    bg_image = ImageTk.PhotoImage(img_file)

    #put the image on a canvas and keep a reference so it doesnt disappear
    canvas = tk.Canvas(frame, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.image = bg_image



    #frame for the login boxes on top of the image
    login_frame = tk.Frame(root, bg="")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")



    #username label and box
    username_label = tk.Label(login_frame, text="Username")
    username_label.grid(row=0, column=0, pady=10, padx=10)


    username_entry = tk.Entry(login_frame, width=40)
    username_entry.grid(row=0, column=1, pady=10, padx=10, )


    #password label and box with the letters hidden
    password_label = tk.Label(login_frame, text="Password")
    password_label.grid(row=1, column=0, pady=10, padx=10)


    password_entry = tk.Entry(login_frame, width=40, show="*")
    password_entry.grid(row=1, column=1, pady=10, padx=10)


    #button that runs the login function
    login_button = tk.Button(login_frame, text="login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=20)



    root.mainloop()