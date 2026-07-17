import tkinter as tk
from tkinter import ttk
from tkinter import font 
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS task(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL)""")
conn.commit()

# Create gui

window = tk.Tk()
window.title("Admin-pannel")
window.geometry("1920x1080")


def load_tasks():
    for widget in canvas_inner.winfo_children():
        widget.destroy

    cursor.execute("SELECT * FROM tasks")
    taks = cursor.fetchall()
    for task in tasks:
        add_task_item(task[0])

#title
header_label = tk.Label(window, text="Mayfair Admin",)
header_label.pack()

Job_frame = tk.Frame(window)
Job_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(Job_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(Job_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_inner = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_inner, anchor="nw")
canvas_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


window.mainloop()