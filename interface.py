import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


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



root.mainloop()