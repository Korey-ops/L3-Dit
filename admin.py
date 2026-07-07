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

#title
header_label = tk.Label(window, text="Mayfair Admin",)
header_label.pack()

window.mainloop()