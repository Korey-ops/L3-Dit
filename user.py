import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import hashlib
import random
import pyautogui


#initialise main window
size = pyautogui.resolution()
root = tk.Tk()
root.title("work forum")
root.geometry("1920x1080")

def user_Frame():



    root = tk.Tk()
    frame = tk.Frame(root)
    frame.place( relx=0.5, rely=0.5, anchor="center")

    user_frame = tk.Frame(root)
    user_frame.pack()



    location_options = ["room1", "room2", "room3", "room4", "room5", "room6", "room7", "room8", "room9", "room10", "room11", "hall"]
    location_drop = ttk.Combobox(user_frame, values=location_options, state="readonly")
    location_drop.set("choose an option")
    location_drop.pack(pady=10)

    class StarRating(user_frame):
        def __init__(self, master, total_stars=5, size=24, initial_rating=0, command=None):
            super().__init__(master)
            self.total_stars = total_stars
            self.size = size
            self.current_rating = initial_rating
            self.command = command  # Optional callback function
        
            self.stars = []
            self.create_widgets()
            self.update_stars(self.current_rating)

        def create_widgets(self):
            """Creates individual labels for each star."""
            for i in range(self.total_stars):
                # Use '★' for standard systems; text labels adapt perfectly to styling
                star = tk.Label(
                    self, 
                    text="☆", 
                    font=("Arial", self.size), 
                    fg="gray", 
                    cursor="hand2"
                )
                star.pack(side="left", padx=2)
            
                # Bind events for hover mechanics and clicking
                star.bind("<Enter>", lambda event, idx=i: self.on_hover(idx))
                star.bind("<Leave>", lambda event: self.on_leave())
                star.bind("<Button-1>", lambda event, idx=i: self.on_click(idx))
            
                self.stars.append(star)

        def update_stars(self, rating_value):
            """Fills stars up to the rating value and leaves the rest empty."""
            for i, star in enumerate(self.stars):
                if i < rating_value:
                    star.config(text="★", fg="#FFD700")  # Filled gold star
                else:
                    star.config(text="☆", fg="gray")     # Empty gray star

        def on_hover(self, index):
            """Highlights stars dynamically up to the hovered index."""
            self.update_stars(index + 1)

        def on_leave(self):
            """Resets the stars back to the last permanently saved click rating."""
            self.update_stars(self.current_rating)

        def on_click(self, index):
            """Permanently saves the rating choice on mouse click."""
            self.current_rating = index + 1
            self.update_stars(self.current_rating)
        
            # Fire callback function if provided
            if self.command:
                self.command(self.current_rating)


    # --- Example Usage Application ---
    if __name__ == "__main__":
        def display_rating(score):
            score_label.config(text=f"Selected Rating: {score} / 5")


        # Context Label
        title = tk.Label(user_Frame, text="Rate your experience:", font=("Arial", 12, "bold"))
        title.pack(pady=5)

        # Instantiate the custom StarRating component
        rating_component = StarRating(user_Frame, total_stars=5, size=28, command=display_rating)
        rating_component.pack(pady=10)

        # Label to capture and show the output value dynamically
        score_label = tk.Label(user_Frame, text="Selected Rating: 0 / 5", font=("Arial", 10))
        score_label.pack(pady=5)





user_Frame




root.mainloop()


