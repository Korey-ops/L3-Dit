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
cursor.execute("""
SELECT id, name, location, type, urgency, task 
FROM jobs
order BY urgency DESC
""")
jobs = cursor.fetchall()
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

def show_job(job):

    job_card = tk.Frame(canvas_inner, relief="raised", bd=2, padx=10, pady=10)
    job_card.pack(fill="x", padx=10, pady=10)

    stars = "★" * job[4] + "☆" * (5-job[4])

    title = tk.Label(job_card, text="f{stars}   {job[2]}")
    title.pack(anchor="w")

    desc = tk.Label(job_card, text=job[5][:60] + "...", anchor="w")
    desc.pack(anchor="w")
    


window.mainloop()