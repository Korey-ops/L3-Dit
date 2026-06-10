import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 1111))




def login():
    username = username_entry.get()
    password = Password_entry.get()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if username and password:
        try:

            client.send((username + "\n").encode())
            client.send((hashed_password + "\n").encode())
        
            response = client.recv(1024).decode()
            print("respons recieved")
            if response == "login successfull!":
                messagebox.showinfo("login", "welcome" + username + "!")
            else:
                messagebox.showerror("login", "Failed")
        except Exception as e:
            messagebox.showerror("Connection error", str(e))
    else:
        messagebox.showwarning("Missing Fields", "Please enter both Username and Passwords")


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


Username_Label = tk.Label(root, text="Username", font=("arial", 12))
Username_Label.place(x=920, y=440)


username_entry = tk.Entry(root, width=40)
username_entry.place(x=840, y=470)


Password_Label = tk.Label(root, text="Password", font=("arial", 12))
Password_Label.place(x=920, y=500)


Password_entry = tk.Entry(root, width=40)
Password_entry.place(x=840, y=530)

Login_button = tk.Button(root, text="login", command=login)
Login_button.place(x=940, y=560 )


root.mainloop()