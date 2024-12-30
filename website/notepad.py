
from flask import Flask
from flask_login import current_user, login_required
from website import badridb  # Absolute import
from website.database import Note  # Absolute import
from website import create_app  # Absolute import
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import sys

# Create the Flask application instance
app = create_app()

# Define the Notepad class
class Notepad:
    def __init__(self, user_id):
        self.user_id = int(user_id)
        print(f"User ID: {self.user_id}")
        self.note = tk.Tk()
        self.note.title("Instant Notes")
        self.note.config(width=300, height=400, bg="#6c7c80", pady=20)
        
        self.notebox = scrolledtext.ScrolledText(wrap=tk.WORD, width=40, height=8, font=("Times New Roman", 15), pady=20, padx=20)
        self.notebox.grid(row=2, column=1, columnspan=10)
        
        self.note_name = tk.Entry()
        self.note_name.grid(row=1, column=1)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'static', 'right.png')
        correct = tk.PhotoImage(file=image_path)
        
        self.save = tk.Button(image=correct, command=self.save_info, bg='#6c7c80', highlightthickness=0)
        self.save.grid(row=1, column=2)
        
        self.note.mainloop()

    def save_info(self):
        info = self.notebox.get("1.0", tk.END)
        note_name = self.note_name.get()
        
        connect = Note(data=info, file_name=note_name, user_id=self.user_id,floder="Multiii Notes")
        badridb.session.add(connect)
        badridb.session.commit()
        
        messagebox.showinfo(title="Saved", message="Your note has been saved successfully")

# Create a Flask application context
with app.app_context():
    # Assuming current_user_info is passed as a command-line argument
    current_user_info = sys.argv[1]
    print(f"Current User Info: {current_user_info}")  # Assuming current_user_info is a string
    notepad = Notepad(current_user_info)
