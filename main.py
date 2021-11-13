import tkinter as tk
import tkinter.ttk as ttk
import requests
from tkinter import messagebox


global auth_token

azure = "https://cinemareservationapi.azurewebsites.net/"
local = "https://localhost:44395/"
def infoBox(msg):
    messagebox.showinfo('info',msg)
def errorBox(msg):
    messagebox.showerror('error',msg)
def AdminPanel():
    def register():
        payload = {
            "email": worker_email_input.get()
        }
        respone_post_worker = requests.post(str(azure + "worker"),json=payload, verify=False)
        if respone_post_worker.status_code != 201:
            infoBox(respone_post_worker.text)

        else:
            infoBox((str(respone_post_worker.status_code) +'\t' + str(worker_email_input.get()) + "\t created succesfuly"))
    def delete():
        if worker_id_label.get() != None:
            respone_post_worker = requests.delete(str(azure + "worker/" + str(worker_id_label.get())), verify=False)
            if respone_post_worker.status_code != 204:
                infoBox(respone_post_worker.text)
        else:
            infoBox('ID cannot be empty')
    admin_window = tk.Tk()
    admin_window.geometry("1000x350")
    admin_window.title("Cinema Login - Admin")
    admin_window.grid_columnconfigure(0, weight=1)
    admin_label = tk.Label(admin_window,
                           text="Create or Delete worker accounts:",
                           font=("Helvetica", 15))
    admin_label.grid(row=0, column=0, sticky="NW", padx=20, pady=10)
    respone_get_worker = requests.get(str(azure + "worker"), verify=False)


    treeview = ttk.Treeview(admin_window, show="headings", columns=("id", "email", "password","role"))
    treeview.heading("#1", text="id")
    treeview.heading("#2", text="email")
    treeview.heading("#3", text="password")
    treeview.heading("#4", text="role")
    treeview.grid(row=1, column=0, sticky="NW", padx=20, pady=10)
    treeview.config(height=len(respone_get_worker.json()))
    for row in respone_get_worker.json():
        treeview.insert("", "end", values=(row["id"], row["email"], row["password"], row["role"]))

    get_button = tk.Button(admin_window,text="Delete User", command=delete)
    get_button.grid(row=4, column=0, sticky="w", padx=200)
    post_button = tk.Button(admin_window,text="Register", command=register)
    post_button.grid(row=5, column=0, sticky="w", padx=200)
    get_button.config(width=100, height=1)
    post_button.config(width=100, height=1)


    worker_email_label = tk.Label(admin_window,
                           text="Email:",
                           font=("Helvetica", 15))
    worker_email_label.grid(row=2, column=0, sticky="w", padx=200, pady=10)
    worker_email_input = tk.Entry(admin_window)
    worker_email_input.grid(row=2, column=0, sticky="w", padx=260, pady=10)
    worker_email_input.config(width=100)
    worker_id_label = tk.Label(admin_window,
                           text="ID:",
                           font=("Helvetica", 15))
    worker_id_label.grid(row=3, column=0, sticky="W", padx=200, pady=10)
    worker_id_label = tk.Entry(admin_window)
    worker_id_label.grid(row=3, column=0, sticky="W", padx=260, pady=10)
    worker_id_label.config(width=100)


def login():
    if email_input.get() and password_input.get():
        email = email_input.get()
        password = password_input.get()
        payload = {"email": email,
                   "password": password}


        response = requests.post(str(azure + "account/login"),
                                    json=payload,verify = False)

        if response.status_code == 200:
            auth_token = response.json()['token']
            try:
                role = response.json()['userDto']['role']['name']
                if role == 'Admin':
                    AdminPanel()
                elif role =='Worker':
                    pass
                else:
                    pass
            except Exception as e:
                print(e)
        else:
            errorBox(response.text)
    else:
        errorBox("Email and Password cannot be empty!")
def register():
    if email_input.get() and password_input.get():
        email = email_input.get()
        password = password_input.get()
        payload = {"email": email,
                   "password": password}


        response = requests.post(str(azure + "user/register"),
                                    json=payload,verify = False)

        if response.status_code == 200:
            infoBox("Succesfuly Registered")
        else:
            errorBox(response.text)
    else:
        errorBox("Email and Password cannot be empty!")

# region login


window = tk.Tk()
window.geometry("500x250")
window.title("Cinema Login")
window.grid_columnconfigure(0, weight=1)
login_label = tk.Label(window,
                             text="Please Login:",
                             font=("Helvetica", 15))
login_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

email_label = tk.Label(window,
                             text="Email:",
                             font=("Helvetica", 15))
email_label.grid(row=1, column=0, sticky="W", padx=100, pady=10)

password_label = tk.Label(window,
                             text="Password:",
                             font=("Helvetica", 15))
password_label.grid(row=2, column=0, sticky="W", padx=100, pady=10)


email_input = tk.Entry(window)
email_input.grid(row=1, column=0, sticky="E", padx=150)
password_input = tk.Entry(window)
password_input.grid(row=2, column=0, sticky="E", padx=150)
password_input.config(show="*");


text_response = "Text Input Can't Be Empty!"

login_button = tk.Button(text="Login", command=login)
login_button.grid(row=3, column=0, sticky="E", padx=200)
register_button = tk.Button(text="Register", command=register)
register_button.grid(row=4, column=0, sticky="E", padx=200)
login_button.config(width=100, height=1)
register_button.config(width=100, height=1)

# endregion


if __name__ == "__main__":
    window.mainloop()






