from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password__ = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password__)
    pyperclip.copy(password__)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_ = web_entry.get()
    email_ = email_entry.get()
    password_ = password_entry.get()
    new_data = {
        website_: {
            "email": email_,
            "password": password_,
        }
    }

    if len(website_) == 0 or len(password_) == 0 or len(email_) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any field empty")

    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            web_entry.delete(0, END)
            password_entry.delete(0, END)
            web_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_ = web_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No datafile found.")

    else:
        if website_ in data:
            email_ = data[website_]["email"]
            password_ = data[website_]["password"]
            pyperclip.copy(password_)
            messagebox.showinfo(title=website_, message=f"Email: {email_}\nPassword: {password_}")

        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_} exists.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website = Label(text="Website:")
website.grid(row=1, column=0)

email = Label(text="Email/Username:")
email.grid(row=2, column=0)

password = Label(text="Password:")
password.grid(row=3, column=0)

web_entry = Entry(width=35)
web_entry.grid(row=1, column=1, columnspan=2)
web_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "xyz@gmail.com")

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)

button = Button(text="Generate Password", width=14, command=generate_password)
button.grid(row=3, column=2)

add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
