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


def open_job_detail(job):
    """Open a popup window showing the full details for one job."""
    job_id, name, location, job_type, urgency, task = job
 
    detail = tk.Toplevel(window)
    detail.title(f"Job #{job_id}")
    detail.geometry("500x400")
 
    tk.Label(detail, text=f"Job #{job_id}", font=("arial", 16, "bold")).pack(pady=(10, 5))
    tk.Label(detail, text=f"Urgency: {urgency}", font=("arial", 12)).pack(anchor="w", padx=15)
    tk.Label(detail, text=f"Name: {name}", font=("arial", 12)).pack(anchor="w", padx=15)
    tk.Label(detail, text=f"Location: {location}", font=("arial", 12)).pack(anchor="w", padx=15)
    tk.Label(detail, text=f"Type: {job_type}", font=("arial", 12)).pack(anchor="w", padx=15)
 
    tk.Label(detail, text="Description:", font=("arial", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
    desc_box = tk.Text(detail, wrap="word", height=10)
    desc_box.insert("1.0", task)
    desc_box.config(state="disabled")
    desc_box.pack(fill="both", expand=True, padx=15, pady=5)
 
    def delete_job():
        if messagebox.askyesno("Confirm", f"Delete job #{job_id}?"):
            cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            conn.commit()
            detail.destroy()
            load_tasks()
 
    button_frame = tk.Frame(detail)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Delete", command=delete_job, bg="#d9534f", fg="white").pack(side="left", padx=5)
    tk.Button(button_frame, text="Close", command=detail.destroy).pack(side="left", padx=5)

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
    job_id, name, location, job_type, urgency, task = job

    job_card = tk.Frame(canvas_inner, relief="raised", bd=2, padx=10, pady=10, cursor="hand2")
    job_card.pack(fill="x", padx=10, pady=5)

    title = tk.Label(job_card, text=f"{urgency}   {name}", anchor="w", font=("arial", 12, "bold"))
    title.pack(anchor="w")

    desc = tk.Label(job_card, text=task[:60] + ("..." if len(task) > 60 else ""), anchor="w")
    desc.pack(anchor="w")
    

def load_tasks():
    for widget in canvas_inner.winfo_children():
        widget.destroy()
 
    cursor.execute("""
        SELECT id, name, location, type, urgency, task
        FROM jobs
        ORDER BY urgency DESC
    """)
    jobs = cursor.fetchall()
 
    if not jobs:
        tk.Label(canvas_inner, text="No jobs submitted yet.", font=("arial", 12)).pack(pady=20)
        return
 
    for job in jobs:
        show_job(job)
window.mainloop()