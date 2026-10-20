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


def login():
    global username, password
    username = username_entry.get().strip()
    password = Password_entry.get()

    if username and password:
        try:
            response = request({"action": "login",
                                "username": username,
                                "password": password})
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

def LogIn_Page():

    global root, username_entry, Password_entry


    #initialise main window
    root = tk.Tk()
    root.title("work forum")
    root.geometry("1920x1080")

    frame = tk.Frame(root)
    frame.place( relx=0.5, rely=0.5, anchor="center")

    Img_file = Image.open("bg.png")
    bg_image = ImageTk.PhotoImage(Img_file)

    canvas = tk.Canvas(frame, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.image = bg_image



    login_frame = tk.Frame(root, bg="")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")



    Username_Label = tk.Label(login_frame, text="Username")
    Username_Label.grid(row=0, column=0, pady=10, padx=10)


    username_entry = tk.Entry(login_frame, width=40)
    username_entry.grid(row=0, column=1, pady=10, padx=10, )


    Password_Label = tk.Label(login_frame, text="Password")
    Password_Label.grid(row=1, column=0, pady=10, padx=10)


    Password_entry = tk.Entry(login_frame, width=40, show="*")
    Password_entry.grid(row=1, column=1, pady=10, padx=10)


    Login_button = tk.Button(login_frame, text="login", command=login)
    Login_button.grid(row=2, column=0, columnspan=2, pady=20)



    root.mainloop()
