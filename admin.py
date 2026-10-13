import tkinter as tk
from tkinter import ttk
from tkinter import font 
from tkinter import messagebox
import sqlite3
import net

def admin_pannel():

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

    root = tk.Tk()
    root.title("Admin-pannel")
    root.geometry("1920x1080")


    def open_job_detail(job):
        """Open a popup window showing the full details for one job."""
        job_id, name, location, job_type, urgency, task = job
 
        detail = tk.Toplevel(root)
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
            if not messagebox.askyesno("Confirm", f"Delete job #{job_id}?"):
                return
            try:
                resp = net.request({"action": f"delete_job", "id": job_id})
            except Exception as e:
                messagebox.showerror("connection error", str(e))
                return
            if resp["ok"]:
                detail.destroy()
                load_tasks()


        button_frame = tk.Frame(detail)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Delete", command=delete_job, bg="#d9534f", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Close", command=detail.destroy).pack(side="left", padx=5)


    def Log_Out():
        try:
            net.request({"action": "logout"})
        except Exception:
            pass
        root.destroy()
        from main import LogIn_Page
        LogIn_Page()

    header_frame = tk.Frame(root, background="#D3D3D3")
    header_frame.pack(anchor="center", fill="x")


    #title
    header_label = tk.Label(header_frame, text="Mayfair Admin", font=("arial", 28), background="#D3D3D3")
    header_label.pack(side="left", padx=35)

    logout = tk.Button(header_frame, text="Log Out", command=Log_Out, font=("arial", 15), background="#D3D3D3")
    logout.pack(side = "right", padx=35, pady=10)

    Job_frame = tk.Frame(root)
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

        title = tk.Label(job_card, text=f"{urgency}   {name}", anchor="w", font=("arial", 25, "bold"))
        title.pack(anchor="w")

        desc = tk.Label(job_card, text=task[:60] + ("..." if len(task) > 60 else ""), anchor="w", font=("arial", 22))
        desc.pack(anchor="w")

        for widget in (job_card, title, desc):
            widget.bind("<Button-1>", lambda e, j=job: open_job_detail(j))
    

    def load_tasks():
        for widget in canvas_inner.winfo_children():
            widget.destroy()

        try:
            resp = net.request({"action": "get_jobs"})
        except Exception as e:
            messagebox.showerror("Connection error", str(e))
            return
        if not resp["ok"]:
            messagebox.showerror("Connection error", resp.get("error", "failed"))
            return

        jobs = resp["jobs"]
        #most urgentfirst, counting the stars
        jobs.sort(key=lambda j: j[4].count("★"), reverse=True)


        if not jobs:
            tk.Label(canvas_inner, text="No jobs submitted yet.", font=("arial", 12)).pack(pady=20)
            return

        for job in jobs:
            show_job(job)

    load_tasks()


    root.mainloop()


if __name__ == "__main__":
    admin_pannel()