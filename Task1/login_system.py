import tkinter as tk #tkinter settings, we took some reference of https://www.geeksforgeeks.org for how some tkinter funtion working
from tkinter import messagebox

class Login:
    def __init__(self, root, nextpage):
        self.root = root
        self.root.title("System Login")
        self.root.geometry("500x300")
        self.nextpage = nextpage #call the start function in main.py

        tk.Label(root, text="Library Management System").pack()
        
        tk.Label(root, text="Username:").pack()
        self.user = tk.Entry(root) #username input box
        self.user.pack()

        tk.Label(root, text="Password:").pack()
        self.pw = tk.Entry(root, show="*") #password input box
        self.pw.pack()

        tk.Button(root, text="Login", command=self.login).pack()

    def login(self):
        if self.user.get() == "admin" and self.pw.get() == "admin": #verify the password correct or not
            self.root.destroy() #close the login page
            self.nextpage() #call the start function in main.py
        else:
            messagebox.showerror("Error", "Invalid Username or Password")