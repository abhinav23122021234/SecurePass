from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_list = (
        [choice(letters) for _ in range(randint(8, 10))] +
        [choice(symbols) for _ in range(randint(2, 4))] +
        [choice(numbers) for _ in range(randint(2, 4))]
    )

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="OOPS", message="Please don't leave any field empty")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)

    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No data file found.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("SecurePass")
window.config(padx=50, pady=50,bg="#2C2F33")

canvas = Canvas(height=200, width=200, bg="#2C2F33", highlightthickness=0)  # match the background color
canvas.create_rectangle(5, 5, 195, 195, outline="#D3D3D3", width=3)  # silver border
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)


# Labels
Label(text="Website:").grid(row=1, column=0, sticky="E")
Label(text="Email/Username:").grid(row=2, column=0, sticky="E")
Label(text="Password:").grid(row=3, column=0, sticky="E")

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1, sticky="W")
website_entry.focus()

email_entry = Entry(width=33)
email_entry.grid(row=2, column=1, columnspan=2, sticky="W")
email_entry.insert(0, "abhi.sharma19jan@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1, sticky="W")

# Buttons
Search_button = Button(text="Search", command=find_password)
Search_button.grid(row=1, column=2, padx=5, sticky="W")

generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(row=3, column=2, padx=5, sticky="W")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
