import tkinter as tk #tkinter settings, we took some reference of https://www.geeksforgeeks.org for how some tkinter funtion working
from tkinter import ttk, messagebox #ttk use for more ui features n tkinter which not provided in tk
from datetime import date, timedelta, datetime
import database #import database from the file
import re #this library only use for matching used in the student id part

#ui part

class DueNotify(tk.Toplevel): #Messagebox warning when student books has overdue
    def __init__(self, root, sid, days, penalty):
        super().__init__(root)
        self.title("Warning")
        self.geometry("400x150")
        self.result = "cancel"
        self.grab_set() #not letting admin to click anything in the main screen until they click any button of the notify box

        msg = ("Student ID: " + str(sid) + "\n" + "The book is overdue by " + str(days) + " days." + "\n" + "Penalty: $" + str(f"{penalty:.2f}")) #f is use for formatting the penalty to 2 s.f.
        
        tk.Label(self, text=msg).pack()

        frame = tk.Frame(self)
        frame.pack()

        tk.Button(frame, text="Cancel", command=self.cancel).pack() #create button
        tk.Button(frame, text="Still return but unpaid", command=self.unpaid, bg="orange").pack() #create button
        tk.Button(frame, text="Paid", command=self.paid, bg="lightgreen").pack() #create button

    def cancel(self):
        self.result = "cancel"
        self.destroy()

    def unpaid(self):
        self.result = "unpaid"
        self.destroy()

    def paid(self):
        self.result = "paid"
        self.destroy()

class System:
    def __init__(self, root):
        self.root = root #main root of the tkinter ui

        #CONFIG SOME AMOUNT HERE
        self.onedayfee = 1.00 #penalty for overdue 1 day
        self.maxfee = 100 #limit of the penalty
        self.borrowdays = 14 #default day for borrowing items in the library
        self.maxborrowlimit = 10 #item borrowing limit for each student

        self.root.title("Library Management System")
        self.root.geometry("1280x720")
        self.data = database.load() #load the data of the database

        self.notebook = ttk.Notebook(root) #notebook is for option ui
        self.notebook.pack()

        self.BandR = ttk.Frame(self.notebook)
        self.books = ttk.Frame(self.notebook)
        self.students = ttk.Frame(self.notebook)
        self.dashboard = ttk.Frame(self.notebook)


        self.notebook.add(self.BandR, text="Borrow/Return")
        self.notebook.add(self.books, text="Books")
        self.notebook.add(self.students, text="Students")
        self.notebook.add(self.dashboard, text="Dashboard")

        self.create_pages() #creating ui

       

    def update(self):
        database.save(self.data) #saves data to the database
        self.refresh_book("")
        self.refresh_student()

    def updatepenalty(self, sid):
        #initialise all things
        student = self.data["students"][sid]
        penowned = student["penalty"]
        newpen = 0.0
        
        dayfee = self.onedayfee
        maxfee = self.maxfee
        today = date.today()

        for bid in student["borrowed"]:
            if bid in self.data["books"]:
                book = self.data["books"][bid]
                if book["due_date"] != None:
                    due_date = datetime.strptime(book["due_date"], "%Y-%m-%d").date()
                    if today > due_date:
                        dayscount = (today - due_date).days
                        newpen += (dayscount * dayfee) #calculate the penalty of a book
                    
        total = penowned + newpen #add all the penalty
        if total > maxfee:
            return maxfee #if > maxfee then just set the penalty to maxfee
        else:
            return total

    
    def create_pages(self):
        self.BRMode = tk.StringVar(value="Borrow") #Default set it to borrow mode
        frame1 = tk.Frame(self.BandR, pady=10)
        frame1.pack()

        tk.Radiobutton(frame1, text="Borrow Book", variable=self.BRMode, value="Borrow", command=self.modechange).pack() #borrow option button
        tk.Radiobutton(frame1, text="Return Book", variable=self.BRMode, value="Return", command=self.modechange).pack() #return option button

        self.bframe = tk.Frame(frame1) 
        self.bframe.pack()
        tk.Label(self.bframe, text="Student ID:").pack()
        self.sid = tk.Entry(self.bframe) #student id input box
        self.sid.pack()

        tk.Button(self.bframe, text="Enter", command=self.borrow).pack() #create button

        self.bframe2 = tk.Frame(self.bframe) 
        
        self.stdinfo = tk.Label(self.bframe2, text="", fg="red") #shows how many books student borrowed and their penalty
        self.stdinfo.pack()
        
        cols = ("Book ID", "Name", "Due Date")
        self.borrow_tree = ttk.Treeview(self.bframe2, columns=cols, show="headings", height=5) #define the headings
        for c in cols: 
            self.borrow_tree.heading(c, text=c)
        self.borrow_tree.pack(fill="x", padx=20, pady=5)

        #ui settings for feature 2: book settings

        frame2 = tk.Frame(self.bframe2)
        frame2.pack()
        tk.Label(frame2, text="Book ID:").pack()
        self.bid = tk.Entry(frame2) #bookid input box
        self.bid.pack()

        tk.Label(frame2, text="Due Date (YYYY-MM-DD):").pack()
        self.duedate = tk.Entry(frame2) #book due date input box
        self.duedate.pack()
        
        tk.Button(frame2, text="Borrow Book", command=self.borrow_book, bg="lightgreen").pack() #create button

        self.rframe = tk.Frame(frame1)

        tk.Label(self.rframe, text="Scan/Enter Book ID:").pack()
        self.return_bookid = tk.Entry(self.rframe) #bookid input box
        self.return_bookid.pack()

        tk.Button(self.rframe, text="Return Book", command=self.return_book, bg="red").pack() #create button

        self.modechange() #initialise the frame
        
        #ui settings for feature 3: book settings
       
        frame3 = tk.Frame(self.books)
        frame3.pack()

        tk.Label(frame3, text="ISBN:").pack()
        self.book_isbn = tk.Entry(frame3) #isbn input box
        self.book_isbn.pack()

        tk.Label(frame3, text="Book Name:").pack()
        self.book_name= tk.Entry(frame3) #book name input box
        self.book_name.pack()

        tk.Label(frame3, text="Author:").pack()
        self.book_author = tk.Entry(frame3) #author input box
        self.book_author.pack()

        tk.Label(frame3, text="Category:").pack()
        self.book_category = tk.Entry(frame3) #book category input box
        self.book_category.pack()

        tk.Button(frame3, text="Add new book", command=self.add_book).pack() #create button

        #ui for the down part of the book searching ui
        
        frame3_2 = tk.Frame(self.books)
        frame3_2.pack()
        tk.Label(frame3_2, text="Search (ISBN/Book name):").pack()
        
        self.book_search = tk.Entry(frame3_2) #isbn/book name input box
        self.book_search.pack()

        tk.Button(frame3_2, text="Search", command=self.search_books).pack() #create button

        tk.Button(frame3_2, text="Delete Selected Book", command=self.delete_book).pack(side="right") #create button

        cols = ("Book ID", "ISBN", "Book Name", "Author", "Category", "Status", "Due Date")
        self.book_tree = ttk.Treeview(self.books, columns=cols, show="headings") #define the headings
        for c in cols: 
            self.book_tree.heading(c, text=c)
        self.book_tree.pack()
        self.refresh_book("")

        #ui settings for feature 4: student settings

        frame4 = tk.Frame(self.students)
        frame4.pack()

        tk.Label(frame4, text="Student ID (start with s):").pack()
        self.student_id = tk.Entry(frame4) #student id input box
        self.student_id.pack()

        tk.Label(frame4, text="Name:").pack()
        self.student_name = tk.Entry(frame4) #student name input box
        self.student_name.pack()

        tk.Button(frame4, text="Add/Update Student", command=self.add_student).pack() #create button
        tk.Button(frame4, text="Delete Selected Student", command=self.delete_student).pack() #create button
        
        tk.Label(frame4, text="Overdue penalty you want to deduct ($):").pack()
        self.pdeducted = tk.Entry(frame4) #penalty to be deducted input box
        self.pdeducted.pack()
       
        tk.Button(frame4, text="Enter", command=self.pdeduct, bg="lightgreen").pack() #create button

        cols = ("Student ID", "Name", "Borrowed Books", "Overdue Penalty ($)")
        self.student_tree = ttk.Treeview(self.students, columns=cols, show="headings") #define the headings
        for c in cols: 
            self.student_tree.heading(c, text=c)
        self.student_tree.pack()
        self.refresh_student()

        #ui settings for feature 5: dashboard

        frame5 = tk.Frame(self.dashboard)
        frame5.pack()

        tk.Button(frame5, text="Most Popular Books", command=self.popbooks).pack() #create button
        tk.Button(frame5, text="Check Penalty", command=self.checkpenalty).pack() #create button
        tk.Button(frame5, text="Payment Logs", command=self.paymentlog).pack() #create button

        self.dtree = ttk.Treeview(self.dashboard, show="headings") #define the headings
        self.dtree.pack()
    
    def modechange(self):
        if self.BRMode.get() == "Borrow": #check is system in borrow mode, if yes, change to return mode
            self.rframe.pack_forget() #hide the frame
            self.bframe.pack()
        else: #change to borrow mode if not
            self.bframe.pack_forget() #hide the frame
            self.rframe.pack()

    def search_books(self):
        search_text = self.book_search.get() #get the text of input box
        self.refresh_book(search_text)

#main function part

    def borrow(self):
        sid = self.sid.get() #get the text of input box
        if sid not in self.data["students"]:
            messagebox.showerror("Error", "Student not found.")
            return  #cannot find student then not run the code below
         
        student = self.data["students"][sid] #find corrsponding student data from the database
        self.bframe2.pack() 
        
        penalty = self.updatepenalty(sid)
        if penalty > 0: #if penalty larger than 0, then show the amount, otherwise show no penalty
            msg2 = "Penalty: $" + str(round(penalty, 2))
        else:
            msg2 = "No Penalty"
            
        status_msg = "Current Borrowed: " + str(len(student["borrowed"])) + "/10  |  " + msg2
        self.stdinfo.config(text=status_msg)
        
        days = self.borrowdays #this is the allow borrow day
        due = date.today() + timedelta(days=days) #current date + xx day
        self.duedate.insert(0, due.strftime("%Y-%m-%d")) #automatically insert the date after the xx day according to the settings

        for r in self.borrow_tree.get_children(): #initialise the tree(delete current items)
            self.borrow_tree.delete(r)
            
        for bid in student["borrowed"]:
            if bid in self.data["books"]: #hshows the books that student borrowed
                targetbook = self.data["books"][bid]
                bname = targetbook["book_name"]
                duedate2 = targetbook["due_date"]
                self.borrow_tree.insert("", "end", values=(bid, bname, duedate2)) #insert book id, name and due date into the tree

    def borrow_book(self):
        sid = self.sid.get() #get the text of input box
        bid = self.bid.get() #get the text of input box
        duedate2 = self.duedate.get() #get the text of input box

        if bid not in self.data["books"]: 
            messagebox.showerror("Error", "Book ID not found.") #if book id not found then return error
            return

        try:
            datetime.strptime(duedate2, "%Y-%m-%d") #try to convert the due date data into javascript format
        except:
            messagebox.showerror("Error", "Invalid Date format. Use YYYY-MM-DD") #if cannot convert, return error
            return

        student = self.data["students"][sid] #get the student data by sid
        book = self.data["books"][bid] #get the book data by bid

        if book["status"] != "Available":
            messagebox.showwarning("Warning", "This book is currently borrowed.")
            return #do not proceed
        
        if len(student["borrowed"]) >= self.maxborrowlimit: #detect student has exceed the max borrow limit or not
            msg = sid + " has already borrowed 10 books. Do you still want to allow this borrow?"
            proceed = messagebox.askyesno("Warning", msg) #ask admin still allow borrow or not
            if proceed == False: 
                return #if not then do not proceed

        penalty = self.updatepenalty(sid) #check is student still has unpaid penalty
        if penalty > 0:
            msg = student["name"] + " has $" + str(round(penalty, 2)) + " unpaid penalty. Do you still want to allow this borrow?"
            proceed = messagebox.askyesno("Warning", msg) #ask admin still allow borrow or not
            if proceed == False: 
                return #if not then do not proceed

        book["status"] = "Borrowed" #set the book status to borrow
        book["due_date"] = duedate2 #set the book duedate according the input of the box
        book["borrowtimes"] = book["borrowtimes"] + 1 
        student["borrowed"].append(bid) #add the book data to the student borrowed book list
        self.bid.delete(0, tk.END) #delete the text of input box, reference: https://www.geeksforgeeks.org/python/how-to-clear-the-entry-widget-after-button-press-in-tkinter/
        self.duedate.delete(0, tk.END) #delete the text of input box, reference: https://www.geeksforgeeks.org/python/how-to-clear-the-entry-widget-after-button-press-in-tkinter/
        self.update() #refresh the tree data
        self.borrow() #update the data of borrow page
        messagebox.showinfo("Done", "Book borrowed sucessfully, due date: " + duedate2)

    def return_book(self):
        bid = self.return_bookid.get() #get the text of input box

        if bid not in self.data["books"]:
            messagebox.showerror("Error", "Invalid Book ID.")
            return

        book = self.data["books"][bid]
        if book["status"] != "Borrowed":
            messagebox.showerror("Error", "This book is not currently borrowed.")
            return

        for sid in self.data["students"]:
            info = self.data["students"][sid]
            if bid in info["borrowed"]:
                student_id = sid
                break #stop the for loop once the target is found

        student = self.data["students"][student_id]
        duedate2 = datetime.strptime(book["due_date"], "%Y-%m-%d").date() #change it to javascript date format
        today = date.today()
        overdue = (today - duedate2).days #calculate how amny days the book has overdue

        if overdue > 0: #make sure it only calculate if the book has overdue
            totalfee = overdue * self.onedayfee #calculate the total fee (overdue days x fee per day)
            
            dialog = DueNotify(self.root, student_id, overdue, totalfee) #generate the notify box
            self.root.wait_window(dialog) #wait until the admin has clicked the button

            if dialog.result == "cancel":
                return 
            elif dialog.result == "unpaid":
                penalty = student["penalty"] + totalfee
                if penalty > self.maxfee:
                    student["penalty"] = self.maxfee
                else:
                    student["penalty"] = penalty
            elif dialog.result == "paid":
                new_record = {} #initialise the container
                new_record["date"] = date.today().strftime("%Y-%m-%d")
                new_record["student_id"] = student_id
                new_record["amount"] = totalfee
                self.data["paymentlog"].append(new_record) #add the pay record to the log

        student["borrowed"].remove(bid) #remove the book from the student borrowed book list
        book["status"] = "Available" #change the book status to available
        book["due_date"] = None #clear the due date of the book
        self.update() #refresh the tree data
        messagebox.showinfo("Done", "Book returned successfully.")


    def add_book(self):
        isbn = self.book_isbn.get() #get the text of input box
        bname = self.book_name.get() #get the text of input box
        
        if isbn == "" or bname == "": 
            messagebox.showerror("Error", "ISBN and Book Name are required.")
            return
        
        new_id = database.bid_gen(self.data) #generate a book id for the new book
        
        new_book = {} #initialise the container
        new_book["isbn"] = isbn
        new_book["book_name"] = bname
        new_book["author"] = self.book_author.get() #get the text of input box
        new_book["category"] = self.book_category.get() #get the text of input box
        new_book["status"] = "Available"
        new_book["borrowtimes"] = 0
        new_book["due_date"] = None
        
        self.data["books"][new_id] = new_book #add the book data to the book list database
        self.update()
        messagebox.showinfo("Done", "Book added successfully! Book ID: " + new_id)
        
    def delete_book(self):
        selected = self.book_tree.selection() #check which row that admin selected
        if len(selected) == 0: 
            messagebox.showerror("Error", "Please select a book from the list!")
            return
        
        bid = self.book_tree.item(selected[0])["values"][0] #get the value of first column (bid)
   
        book = self.data["books"][bid] #get the book data by bid
        if book["status"] == "borrowed": #if the book deleted when students still borrowing, then system unable to return due to the book not found
            messagebox.showerror("Error", "Cannot delete this book because it is currently borrowed by a student.") 
            return
            
        del self.data["books"][bid] #delete the book data from the book list database
        self.update() #refresh the tree data
        messagebox.showinfo("Done", "Book has deleted.")


    def refresh_book(self, searchtext):
        for i in self.book_tree.get_children(): 
            self.book_tree.delete(i) #delete all items in the book tree
            
        for bid in self.data["books"]:
            info = self.data["books"][bid] #get the book data of each book by their book id
            
            if searchtext in info["book_name"] or searchtext in info["isbn"]: #do search if searchtex has text
                if info["due_date"] == None: #if has due date, directly insert the date, else it will show N/A
                    self.book_tree.insert("", "end", values=(bid, info["isbn"], info["book_name"], info["author"], info["category"], info["status"], "N/A"))
                else:
                    self.book_tree.insert("", "end", values=(bid, info["isbn"], info["book_name"], info["author"], info["category"], info["status"], info["due_date"]))


    def add_student(self):
        sid = self.student_id.get() #get the text of input box
        if bool(re.match(r'^s\d{7}$', sid)) == False: #check is it match the format, our reference: https://www.w3schools.com/python/ref_module_re.asp
            messagebox.showerror("Error", "Student ID must start with 's' followed by exactly 7 digits.")
            return
            
        if sid not in self.data["students"]: #check is the sid already existed or not
            new_student = {} #initialise the container
            new_student["name"] = self.student_name.get() #get the student name entered in the input box
            new_student["borrowed"] = [] #initialise the list
            new_student["penalty"] = 0.0 #initialise
            self.data["students"][sid] = new_student #save the student data to the database
        else:
            self.data["students"][sid]["name"] = self.student_name.get() #if sid existed, just save the updated student name data to the database
            
        self.update() #refresh the tree data
        messagebox.showinfo("Done", "Student saved.")

    def delete_student(self):
        selected = self.student_tree.selection() #check which row that admin selected
        if len(selected) == 0: #if not selected anything then return error
            messagebox.showerror("Error", "Please select a student!")
            return
            
        sid = self.student_tree.item(selected[0])["values"][0] #get the value of first column (bid)
        student = self.data["students"][sid]
        
        if len(student["borrowed"]) > 0: #if > 0, means student still have borrowed books
            messagebox.showerror("Error", "Unable to delete the student data. Student still borrowing at least 1 book(s)")
            return
            
        penalty = self.updatepenalty(sid)
        if penalty > 0: #if > 0, means student still have unpaid penalty
            msg = "Unable to delete the student data. Student still have unpaid penalty ($" + str(round(penalty, 2)) + ")."
            messagebox.showerror("Error", msg)
            return
            
        del self.data["students"][sid] #delete the student data from the student list database
        self.update() #refresh the tree data
        messagebox.showinfo("Done", "Student deleted.")


    def pdeduct(self):
        selected = self.student_tree.selection() #check which row that admin selected
        if len(selected) == 0: #if not selected anything then return error
            messagebox.showerror("Error", "Select a student.")
            return
            
        sid = self.student_tree.item(selected[0])["values"][0] #get the value of first column (bid)
        amo = float(self.pdeducted.get()) #get the custom amount of penalty input box

        if amo > self.data["students"][sid]["penalty"]: #if the amount deducted > student current penalty then return error
            messagebox.showinfo("Error", "Student remaining penalty cannot lower than 0.")
            return

        if (self.data["students"][sid]["penalty"]) > 0:
            new_record = {} #initialise the container
            new_record["date"] = date.today().strftime("%Y-%m-%d") #get the date of today and convert to more user-friendly format
            new_record["student_id"] = sid
            new_record["amount"] = amo
            self.data["paymentlog"].append(new_record) #add the record to the list
            self.data["students"][sid]["penalty"] -= amo #update the penalty amount in database
            self.update() #refresh the tree data
            messagebox.showinfo("Done", "Penalty deduction success.")
        else:
            messagebox.showinfo("Error", "Student remaining penalty cannot lower than 0.")

    def refresh_student(self):
        for r in self.student_tree.get_children(): 
            self.student_tree.delete(r) #delete the original student tree data
            
        for sid in self.data["students"]:
            info = self.data["students"][sid] #get the student info by sid
            penalty = self.updatepenalty(sid)
            bookid = ""
            for i in info["borrowed"]: #check student each borrowed book data
                if bookid == "":
                    bookid = i 
                else:
                    bookid = bookid + ", " + i #add all borrowed book data into a string
            
            totalpenalty = "$" + str(round(penalty, 2))
            self.student_tree.insert("", "end", values=(sid, info["name"], bookid, totalpenalty))


    def popbooks(self):
        for r in self.dtree.get_children():
            self.dtree.delete(r) #delete all items in dashboard tree
            
        self.dtree["columns"] = ("Rank", "Book ID", "ISBN", "Book Name", "Times Borrowed")
        for c in self.dtree["columns"]: 
            self.dtree.heading(c, text=c) #make these columns be the heading of the tree

        def gettimes(book):
            return book[1]["borrowtimes"] #return the borrow time for each books

        booklist = list(self.data["books"].items()) #fetch the whole book list from the database and put it in a list
        booklist.sort(key=gettimes, reverse=True) #sort according to the times borrowed, reference: https://www.w3schools.com/python/ref_list_sort.asp
        
        rank = 1 #start from rank 1 of the times borrowed
        for book in booklist:
            bid = book[0]
            info = book[1]
            self.dtree.insert("", "end", values=(rank, bid, info["isbn"], info["book_name"], info["borrowtimes"]))
            rank = rank + 1

    def checkpenalty(self):
        for r in self.dtree.get_children():
            self.dtree.delete(r) #delete all items in dashboard tree
            
        self.dtree["columns"] = ("Student ID", "Name", "Penalty")
        for c in self.dtree["columns"]: 
            self.dtree.heading(c, text=c) #make these columns be the heading of the tree

        for sid in self.data["students"]:
            info = self.data["students"][sid]
            penalty = self.updatepenalty(sid) #check every student penalty
            if penalty > 0: #if student has a penalty, then insert their data
                totalpenalty = "$" + str(round(penalty, 2))
                self.dtree.insert("", "end", values=(sid, info["name"], totalpenalty))

    def paymentlog(self):
        for r in self.dtree.get_children():
            self.dtree.delete(r) #delete all original data of the payment log list
            
        self.dtree["columns"] = ("Date", "Student ID", "Student Name", "Penalty Paid")
        for c in self.dtree["columns"]: 
            self.dtree.heading(c, text=c)  #make these columns be the heading of the tree

        logs = self.data["paymentlog"]
        logslength = len(logs)
        
        for i in range(logslength - 1, -1, -1):
            record = logs[i]
            if record["student_id"] in self.data["students"]: #only check their penalty if student id still existed in the database
                amount = str(round(record["amount"], 2))
            self.dtree.insert("", "end", values=(record["date"], record["student_id"], self.data["students"][record["student_id"]]["name"], "$" + amount))

    