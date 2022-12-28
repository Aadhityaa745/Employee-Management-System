from tkinter import *
from tkinter import ttk
from pymysql import connect
from tkinter import messagebox

con = connect(user='root', password='Aadhi@745', host='localhost', port=3306, db='Aadhityaa')
cur = con.cursor()
# Functions for adding , updating,dele
def add_employee():
    try:
        id_val = int(ID.get())
        name_val = name.get()
        age_val = int(age.get())
        doj_val = doj.get()
        email_val = email.get()
        gen_val = gender.get()
        contact_val = int(contact.get())
        address = txtAddress.get(1.0, END)

        details = (id_val, name_val, age_val, doj_val, email_val, gen_val, contact_val, address)
        for li in details:
            if li == "" or li == 0 or li == None:
                messagebox.showerror("Error", "Enter all fields")
                break
            # To check whether the entered mail id is valid or not
            if "@" not in email_val or "." not in email_val:
                messagebox.showwarning("Invalid entry", "Enter the correct mail id.")
                break
        else:
            # To check whether the id is present in the database or not
            cur.execute('select id from registration')
            for a in cur:
                if a[0] == id_val:
                    messagebox.showerror("Error", "Sorry don't use the id number that already exists!")
                    break
            else:
                qur = "insert into registration values (%s,%s,%s,%s,%s,%s,%s,%s)"
                cur.execute(qur, details)
                con.commit()
                fetch_data()
                messagebox.showinfo("Success", "Successfully registered Employee Data")
                clearAll()

    except:
        messagebox.showerror("Error", "Sorry use the correct inputs for each of the fields!")

def update_employee():
    id_val = int(ID.get())
    name_val = name.get()
    age_val = int(age.get())
    doj_val = doj.get()
    email_val = email.get()
    gen_val = gender.get()
    contact_val = int(contact.get())
    address = txtAddress.get(1.0, END)

    try:
        # To check whether the entered mail id is valid or not
        if "@" not in email_val or "." not in email_val:
            messagebox.showwarning("Invalid entry", "Enter the correct mail id.")
            exit()
        cur.execute("update registration set name=%s, age=%s, doj=%s, email=%s, gender=%s, contact=%s,"
                            "address=%s where id=%s", (name_val, age_val, doj_val, email_val, gen_val, contact_val,
                                                       address, id_val))
        con.commit()
        messagebox.showinfo("Success", "Successfully Updated Employee Data")
        clearAll()
        fetch_data()
        txtID.focus()

    except:
        messagebox.showerror("Error", "Sorry use the correct inputs for each of the fields!")

def get_data(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    ID.set(row[0])
    name.set(row[1])
    age.set(row[2])
    doj.set(row[3])
    email.set(row[4])
    gender.set(row[5])
    contact.set(row[6])
    txtAddress.delete(1.0, END)
    txtAddress.insert(END, row[7])

def fetch_data():
    con = connect(user='root', password='Aadhi@745', host='localhost', port=3306, db='Aadhityaa')
    cur = con.cursor()
    cur.execute("select * from registration")
    rows = cur.fetchall()
    if len(rows) != 0:
        tv.delete(*tv.get_children())
        for row in rows:
            tv.insert('', END, values=row)
    con.commit()

def delete_employee():
    try:
        ID = txtID.get()
        query = "delete from registration where id = %s"
        cur.execute(query, ID)
        con.commit()
        messagebox.showinfo("Success", "Successfully deleted employee data from the database")
        clearAll()
        fetch_data()

    except:
        messagebox.showerror("Error", "Select the correct ID to delete data")

def clearAll():
    ID.set("")
    name.set("")
    age.set("")
    doj.set("")
    email.set("")
    gender.set("")
    contact.set("")
    txtAddress.delete(1.0, END)

page = Tk()
page.title("Employee Management System")
page.geometry("1500x1500")
page.config(bg="#2c3e50")
page.state("zoomed")

ID = IntVar()
name = StringVar()
age = IntVar()
doj = StringVar()
gender = StringVar()
email = StringVar()
contact = IntVar()

# Entries Frame
entries_frame = Frame(page, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Employee Management System", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblName = Label(entries_frame, text="Name     :", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=8, pady=8, sticky="w")
txtName = Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=20)
txtName.place(x=100, y=85, )

lblAge = Label(entries_frame, text="Age               :", font=("Calibri", 16), bg="#535c68", fg="white")
lblAge.grid(row=1, column=2, padx=10, pady=10, sticky="w")
txtAge = Entry(entries_frame, textvariable=age, font=("Calibri", 16), width=20)
txtAge.place(x=500, y=85, )

lbldoj = Label(entries_frame, text="D.O.J      :", font=("Calibri", 16), bg="#535c68", fg="white")
lbldoj.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtDOJ = Entry(entries_frame, textvariable=doj, font=("Calibri", 16), width=20)
txtDOJ.place(x=100, y=135, )

lblEmail = Label(entries_frame, text="Email            :", font=("Calibri", 16), bg="#535c68", fg="white")
lblEmail.grid(row=2, column=2, padx=10, pady=10, sticky="w")
txtEmail = Entry(entries_frame, textvariable=email, font=("Calibri", 16), width=20)
txtEmail.place(x=500, y=135, )

lblGender = Label(entries_frame, text="Gender  :", font=("Calibri", 16), bg="#535c68", fg="white")
lblGender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
comboGender = ttk.Combobox(entries_frame, font=("Calibri", 16), width=18, textvariable=gender, state="readonly",
                           values=('Male', 'Female'))
comboGender.place(x=100, y=185, )

lblID = Label(entries_frame, text="ID           :", font=("Calibri", 16), bg="#535c68", fg="white")
lblID.grid(row=4, column=0, padx=10, pady=10, sticky="w")
txtID = Entry(entries_frame, textvariable=ID, font=("Calibri", 16), width=5)
txtID.place(x=100, y=240, )

lblContact = Label(entries_frame, text="Contact No. :", font=("Calibri", 16), bg="#535c68", fg="white")
lblContact.grid(row=3, column=2, padx=10, pady=10, sticky="w")
txtContact = Entry(entries_frame, textvariable=contact, font=("Calibri", 16), width=20)
txtContact.place(x=500, y=185, )

lblAddress = Label(entries_frame, text="Address        :", font=("Calibri", 16), bg="#535c68", fg="white")
lblAddress.grid(row=5, column=2, padx=10, pady=10, sticky="w")
txtAddress = Text(entries_frame, width=50, height=3, font=("Calibri", 16))
txtAddress.place(x=500, y=240, )

# Buttons
btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.place(x=750, y=120, )

Button(btn_frame, command=add_employee, text="Add Details", width=15, height=2, font=("Calibri", 16, "bold"),
       fg="white", bg="#16a085", bd=0).grid(row=0, column=0)
Button(btn_frame, command=update_employee, text="Update Details", width=15, height=2,
       font=("Calibri", 16, "bold"), fg="white", bg="#2980b9", bd=0).grid(row=0, column=1, padx=10)
Button(btn_frame, command=delete_employee, text="Delete Details", width=15, height=2,
       font=("Calibri", 16, "bold"), fg="white", bg="#c0392b", bd=0).grid(row=0, column=2, padx=10)
Button(btn_frame, command=clearAll, text="Clear Details", width=15, height=2,
       font=("Calibri", 16, "bold"), fg="white", bg="#f39c12", bd=0).grid(row=0, column=3, padx=10)

# Table Frame
tree_frame = Frame(page, bg="#ecf0f1")
tree_frame.place(x=0, y=330, width=1535, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width=2)
tv.heading("2", text="Name")
tv.heading("3", text="Age")
tv.column("3", width=2)
tv.heading("4", text="D.O.J")
tv.column("4", width=10)
tv.heading("5", text="Email")
tv.heading("6", text="Gender")
tv.column("6", width=10)
tv.heading("7", text="Contact")
tv.column("7", width=45)
tv.heading("8", text="Address")
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", get_data)
tv.pack(fill=X)

fetch_data()
page.mainloop()