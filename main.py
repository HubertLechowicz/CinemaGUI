import tkinter as tk
import tkinter.ttk as ttk
import requests
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import tktimepicker
import tkcalendar
from tktimepicker import constants
from datetime import datetime
import json
auth_token = None
unresizable = True
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
        if worker_id_input.get() != None:
            respone_post_worker = requests.delete(str(azure + "worker/" + str(worker_id_input.get())), verify=False)
            if respone_post_worker.status_code != 204:
                infoBox(respone_post_worker.text)
            else:
                infoBox(("Deleted user with id  " + str(worker_id_input.get() + " succesfuly")))
        else:
            infoBox('ID cannot be empty')

    admin_window = tk.Tk()
    admin_window.geometry("1000x350")
    if unresizable:
        admin_window.resizable(width=0, height=0)
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
    worker_id_input = tk.Entry(admin_window)
    worker_id_input.grid(row=3, column=0, sticky="W", padx=260, pady=10)
    worker_id_input.config(width=100)
def WorkerPanel():
    def movies():
        def post_movie():
            if title_input.get() and lenght_input.get():
                print(len(title_input.get()),lenght_input.get())
                payload = {
                    "name": title_input.get(),
                    "durationInMinutes": int(lenght_input.get())
                }
                respone_post_worker = requests.post(str(azure + "/movie"),json=payload, verify=False)
                if respone_post_worker.status_code != 201:
                    infoBox(respone_post_worker.text)
                else:
                    infoBox("Added '" + title_input.get() + "'" + " with sucess")
            else:
                infoBox('title and lenght cannont be empty')
        movies_window = tk.Tk()
        movies_window.geometry("500x250")
        movies_window.title("Cinema Login - Worker - Movies - Add")
        movies_window.grid_columnconfigure(0, weight=1)


        movies_label = tk.Label(movies_window,
                               text="Add Movie:",
                               font=("Helvetica", 15))
        movies_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

        lenght_label = tk.Label(movies_window,
                               text="Lenght:",
                               font=("Helvetica", 15))
        lenght_label.grid(row=2, column=0, sticky="W", padx=100, pady=10)

        title_label = tk.Label(movies_window,
                                  text="Title:",
                                  font=("Helvetica", 15))
        title_label.grid(row=1, column=0, sticky="W", padx=100, pady=10)

        lenght_input = tk.Entry(movies_window)
        lenght_input.grid(row=2, column=0, sticky="E", padx=150)
        title_input = tk.Entry(movies_window)
        title_input.grid(row=1, column=0, sticky="E", padx=150)

        text_response = "Text Input Can't Be Empty!"

        login_button = tk.Button(movies_window, text="Add Movie", command=post_movie)
        login_button.grid(row=3, column=0, sticky="E", padx=200)
    def rooms():
        def post_room():
            if name_input.get() and lenght_input.get() and size_input.get() :
                payload = {
                    "name": name_input.get(),
                    "seatsCount": int(size_input.get()),
                    "cleaningTimeInMinutes": int(lenght_input.get())
                }

                respone_post_worker = requests.post(str(azure + "/room"),json=payload, verify=False)
                if respone_post_worker.status_code != 201:
                    infoBox(respone_post_worker.text)
                else:
                    infoBox("Added '" + name_input.get() + "' with " + size_input.get() + " seats sucessfuly")
            else:
                infoBox('Name, seats no. and break time fields cannont be empty')
        rooms_window = tk.Tk()
        rooms_window.geometry("500x250")
        rooms_window.title("Cinema Login - Worker - Rooms - Add")
        rooms_window.grid_columnconfigure(0, weight=1)


        movies_label = tk.Label(rooms_window,
                               text="Add Room:",
                               font=("Helvetica", 15))
        movies_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

        lenght_label = tk.Label(rooms_window,
                               text="Break Time:",
                               font=("Helvetica", 15))
        lenght_label.grid(row=2, column=0, sticky="W", padx=100, pady=10)
        size_label = tk.Label(rooms_window,
                               text="Seats:",
                               font=("Helvetica", 15))
        size_label.grid(row=3, column=0, sticky="W", padx=100, pady=10)
        name_label = tk.Label(rooms_window,
                                  text="Name:",
                                  font=("Helvetica", 15))
        name_label.grid(row=1, column=0, sticky="W", padx=100, pady=10)

        lenght_input = tk.Entry(rooms_window)
        lenght_input.grid(row=2, column=0, sticky="E", padx=150)
        name_input = tk.Entry(rooms_window)
        name_input.grid(row=1, column=0, sticky="E", padx=150)
        size_input = tk.Entry(rooms_window)
        size_input.grid(row=3, column=0, sticky="E", padx=150)

        login_button = tk.Button(rooms_window, text="Add Room", command=post_room)
        login_button.grid(row=4, column=0, sticky="E", padx=200)
    def seances():
        def post_seance():
            if movie_id_input.get() and room_id_input.get():

                hour = str(time_input.hours())
                minutes = str(time_input.minutes())
                if time_input.period() =='a.m':
                    ampm = 'am'
                elif time_input.period() == 'p.m':
                    ampm = 'pm'
                date_time = (date_input.get() +'/'+hour+'/'+minutes+'/'+ampm)
                date_time = datetime.strptime(date_time, '%m/%d/%y/%I/%M/%p')
                date_time = date_time.isoformat()
                payload = {
                    "roomId": room_id_input.get(),
                    "movieId": movie_id_input.get(),
                    "dateTime": date_time
                }
                respone_post_seance = requests.post(str(azure + "/seance"), json=payload, verify=False)
                print(payload,'\n',respone_post_seance.status_code,'\n',respone_post_seance.content)
                if respone_post_seance.status_code != 201:
                    infoBox(respone_post_seance.text)
                else:
                    infoBox("Added seance of movie " +movie_id_input.get() +" in room "+ room_id_input.get()+  " with sucess")
            else:
                infoBox('Fields cannont be empty')

        seances_window = tk.Tk()
        seances_window.geometry("700x250")
        seances_window.title("Cinema Login - Worker - Seances - Add")
        seances_window.grid_columnconfigure(0, weight=1)

        seances_label = tk.Label(seances_window,
                                 text="Add seances:",
                                 font=("Helvetica", 15))
        seances_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

        movie_id_label = tk.Label(seances_window,
                                  text="MovieID:",
                                  font=("Helvetica", 15))
        movie_id_label.grid(row=2, column=0, sticky="W", padx=100, pady=10)

        room_id_label = tk.Label(seances_window,
                                 text="RoomID:",
                                 font=("Helvetica", 15))
        room_id_label.grid(row=1, column=0, sticky="W", padx=100, pady=10)

        date_label = tk.Label(seances_window,
                                 text="Date:",
                                 font=("Helvetica", 15))
        date_label.grid(row=3, column=0, sticky="W", padx=100, pady=10)
        date_input = DateEntry(seances_window, width=12, borderwidth=2,sticky='W')
        date_input.grid(row=3,column=0,padx=150)

        time_label = tk.Label(seances_window,
                              text="Time:",
                              font=("Helvetica", 15))
        time_label.grid(row=4, column=0, sticky="W", padx=100, pady=10)

        time_input = tktimepicker.SpinTimePickerOld(seances_window)
        time_input.grid(row=4, column=0, padx=150)
        time_input.addAll(constants.HOURS12)
        time_input.grid(row=4,column=0,sticky='E', padx=100, pady=10)

        movie_id_input = tk.Entry(seances_window)
        movie_id_input.grid(row=2, column=0, sticky="E", padx=300)
        room_id_input = tk.Entry(seances_window)
        room_id_input.grid(row=1, column=0, sticky="E", padx=300)

        login_button = tk.Button(seances_window, text="Add Seances", command=post_seance)
        login_button.grid(row=5, column=0, sticky="E", padx=200)
    def list_movies():
        def movie_delete():
            if movie_id_input.get():
                respone_delete_movie = requests.delete(str(azure + "movie/" + str(movie_id_input.get())), verify=False)
                if respone_delete_movie.status_code != 204:
                    infoBox(respone_delete_movie.text)
                else:
                    infoBox(("Deleted movie with id  " + str(movie_id_input.get() + " succesfuly")))
            else:
                infoBox('ID cannot be empty')
        list_movies_window = tk.Tk()
        list_movies_window.geometry("800x350")
        list_movies_window.title("Cinema Login - Worker - Movies - List")
        list_movies_window.grid_columnconfigure(0, weight=1)
        list_movies_label = tk.Label(list_movies_window,
                               text="List and delete movies:",
                               font=("Helvetica", 15))
        list_movies_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

        respone_get_worker = requests.get(str(azure + "movie"), verify=False)

        treeviewMovies = ttk.Treeview(list_movies_window, show="headings", columns=("id", "name", "durationInMinutes"))
        treeviewMovies.heading("#1", text="id")
        treeviewMovies.heading("#2", text="name")
        treeviewMovies.heading("#3", text="durationInMinutes")
        treeviewMovies.grid(row=1, column=0, sticky="N", padx=20, pady=10)
        treeviewMovies.config(height=len(respone_get_worker.json()))
        for row in respone_get_worker.json():
            treeviewMovies.insert("", "end", values=(row["id"], row["name"], row["durationInMinutes"]))

        del_button = tk.Button(list_movies_window, text="Delete Movie", command=movie_delete)
        del_button.grid(row=3, column=0, sticky="n", padx=200)

        movie_id_label = tk.Label(list_movies_window,
                                   text="ID:",
                                   font=("Helvetica", 15))
        movie_id_label.grid(row=2, column=0, sticky="W", padx=200, pady=10)
        movie_id_input = tk.Entry(list_movies_window)
        movie_id_input.grid(row=2, column=0, sticky="W", padx=260, pady=10)
        movie_id_input.config(width=100)
    def list_rooms():
        def room_delete():
            if room_id_input.get():
                respone_delete_movie = requests.delete(str(azure + "room/" + str(room_id_input.get())), verify=False)
                if respone_delete_movie.status_code != 204:
                    infoBox(respone_delete_movie.text)
                else:
                    infoBox(("Deleted room with id  " + str(room_id_input.get() + " succesfuly")))
            else:
                infoBox('ID cannot be empty')
        list_rooms_window = tk.Tk()
        list_rooms_window.geometry("800x350")
        list_rooms_window.title("Cinema Login - Worker - Movies - List")
        list_rooms_window.grid_columnconfigure(0, weight=1)
        list_rooms_label = tk.Label(list_rooms_window,
                               text="List and delete rooms:",
                               font=("Helvetica", 15))
        list_rooms_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

        respone_get_worker = requests.get(str(azure + "room"), verify=False)
        treeviewRooms = ttk.Treeview(list_rooms_window, show="headings", columns=("id", "name","seatsCount", "cleaningTimeInMinutes"))
        treeviewRooms.heading("#1", text="id")
        treeviewRooms.heading("#2", text="name")
        treeviewRooms.heading("#3", text="seatsCount")
        treeviewRooms.heading("#4", text="cleaningTimeInMinutes")
        treeviewRooms.grid(row=1, column=0, sticky="N", padx=20, pady=10)
        treeviewRooms.config(height=len(respone_get_worker.json()))
        for row in respone_get_worker.json():
            treeviewRooms.insert("", "end", values=(row["id"], row["name"],row["seatsCount"], row["cleaningTimeInMinutes"]))

        del_button = tk.Button(list_rooms_window, text="Delete Room", command=room_delete)
        del_button.grid(row=3, column=0, sticky="n", padx=200)

        room_id_label = tk.Label(list_rooms_window,
                                   text="ID:",
                                   font=("Helvetica", 15))
        room_id_label.grid(row=2, column=0, sticky="W", padx=200, pady=10)
        room_id_input = tk.Entry(list_rooms_window)
        room_id_input.grid(row=2, column=0, sticky="W", padx=260, pady=10)
        room_id_input.config(width=100)
    def list_seances():
        def seance_delete():
            if seance_id_input.get():
                respone_delete_movie = requests.delete(str(azure + "seance/" + str(seance_id_input.get())), verify=False)
                if respone_delete_movie.status_code != 204:
                    infoBox(respone_delete_movie.text)
                else:
                    infoBox(("Deleted seance with id  " + str(seance_id_input.get() + " succesfuly")))
            else:
                infoBox('ID cannot be empty')

        list_seances_window = tk.Tk()
        list_seances_window.geometry("800x350")
        list_seances_window.title("Cinema Login - Worker - Movies - List")
        list_seances_window.grid_columnconfigure(0, weight=1)
        list_seances_label = tk.Label(list_seances_window,
                                    text="List and delete seances:",
                                    font=("Helvetica", 15))
        list_seances_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

        respone_get_worker = requests.get(str(azure + "seance"), verify=False)
        treeviewSeances = ttk.Treeview(list_seances_window, show="headings",
                                     columns=("id", "dateTime", "roomId", "movieId"))
        treeviewSeances.heading("#1", text="id")
        treeviewSeances.heading("#2", text="dateTime")
        treeviewSeances.heading("#3", text="roomId")
        treeviewSeances.heading("#4", text="movieId")
        treeviewSeances.grid(row=1, column=0, sticky="N", padx=20, pady=10)
        treeviewSeances.config(height=len(respone_get_worker.json()))
        for row in respone_get_worker.json():
            treeviewSeances.insert("", "end",
                                 values=(row["id"], row["dateTime"], row["roomId"], row["movieId"]))

        del_button = tk.Button(list_seances_window, text="Delete Seance", command=seance_delete)
        del_button.grid(row=3, column=0, sticky="n", padx=200)

        seance_id_label = tk.Label(list_seances_window,
                                 text="ID:",
                                 font=("Helvetica", 15))
        seance_id_label.grid(row=2, column=0, sticky="W", padx=200, pady=10)
        seance_id_input = tk.Entry(list_seances_window)
        seance_id_input.grid(row=2, column=0, sticky="W", padx=260, pady=10)
        seance_id_input.config(width=100)
    worker_window = tk.Tk()
    worker_window.geometry("520x150")
    if unresizable:
        worker_window.resizable(width=0, height=0)
    worker_window.title("Cinema - Worker")
    worker_window.grid_columnconfigure(0, weight=1)
    admin_label = tk.Label(worker_window,
                           text="Manage movies, rooms, seances :",
                           font=("Helvetica", 15))
    admin_label.grid(row=0, column=0, sticky="NW", padx=50, pady=10)


    movie_button = tk.Button(worker_window,text="Add Movies", command=movies)
    movie_button.grid(row=4, column=0, sticky="nw", padx=215)
    room_button = tk.Button(worker_window,text="Add Rooms", command=rooms)
    room_button.grid(row=5, column=0, sticky="nw", padx=215)
    seance_button = tk.Button(worker_window,text="Add Seances", command=seances)
    seance_button.grid(row=6, column=0, sticky="nw", padx=215)
    movie_button.config(width=15, height=1)
    room_button.config(width=15, height=1)
    seance_button.config(width=15, height=1)

    movie_list_button = tk.Button(worker_window,text="List Movies", command=list_movies)
    movie_list_button.grid(row=4, column=0, sticky="nw", padx=100)
    room_list_button = tk.Button(worker_window,text="List Rooms", command=list_rooms)
    room_list_button.grid(row=5, column=0, sticky="nw", padx=100)
    seance_list_button = tk.Button(worker_window,text="List Seances", command=list_seances)
    seance_list_button.grid(row=6, column=0, sticky="nw", padx=100)
    movie_list_button.config(width=15, height=1)
    room_list_button.config(width=15, height=1)
    seance_list_button.config(width=15, height=1)
def UserPanel():
    def rereve():
        payload = {
            "seanceID": ID_input.get(),
            "count": tickets_no_input.get()
        }
        headers = {'content-type': 'application/json','Authorization': str('Bearer ' + auth_token)}
        respone_user_reserve = requests.post(str(azure + "Reserve"), json=payload,headers=headers ,verify=False)
        if respone_user_reserve.status_code != 201:
            infoBox(respone_user_reserve.text)

        else:
            infoBox(
                ("Reserved " + tickets_no_input.get()+  " seats for " + ID_input.get() + " succesfuly"))
    user_seances_window = tk.Tk()
    user_seances_window.geometry("800x350")
    user_seances_window.title("Cinema Login - User - Reservations")
    user_seances_window.grid_columnconfigure(0, weight=1)
    list_seances_label = tk.Label(user_seances_window,
                                  text="List seances and reserve tickets:",
                                  font=("Helvetica", 15))
    list_seances_label.grid(row=0, column=0, sticky="N", padx=20, pady=10)

    respone_get_worker = requests.get(str(azure + "seance"), verify=False)
    treeviewSeancesUser = ttk.Treeview(user_seances_window, show="headings",
                                   columns=("id", "dateTime", "roomId", "movieId"))
    treeviewSeancesUser.heading("#1", text="id")
    treeviewSeancesUser.heading("#2", text="dateTime")
    treeviewSeancesUser.heading("#3", text="roomId")
    treeviewSeancesUser.heading("#4", text="movieId")
    treeviewSeancesUser.grid(row=1, column=0, sticky="N", padx=20, pady=10)
    treeviewSeancesUser.config(height=len(respone_get_worker.json()))
    for row in respone_get_worker.json():
        treeviewSeancesUser.insert("", "end",
                               values=(row["id"], row["dateTime"], row["roomId"], row["movieId"]))
    ID_label = tk.Label(user_seances_window,
                                  text="Seance ID:",
                                  font=("Helvetica", 15))
    ID_label.grid(row=2, column=0, sticky="w", padx=200, pady=10)
    ID_input = tk.Entry(user_seances_window)
    ID_input.grid(row=2, column=0, sticky="w", padx=340, pady=10)
    ID_input.config(width=100)
    tickets_no_label = tk.Label(user_seances_window,
                               text="Tickets count:",
                               font=("Helvetica", 15))
    tickets_no_label.grid(row=3, column=0, sticky="W", padx=200, pady=10)
    tickets_no_input = tk.Entry(user_seances_window)
    tickets_no_input.grid(row=3, column=0, sticky="W", padx=340, pady=10)
    tickets_no_input.config(width=100)
    get_button = tk.Button(user_seances_window, text="Reserve Seats", command=rereve)
    get_button.grid(row=4, column=0, sticky="w", padx=200)
    get_button.config(width=100, height=1)
    get_button.config(width=100, height=1)
def login():
    if email_input.get() and password_input.get():
        email = email_input.get()
        password = password_input.get()
        payload = {"email": email,
                   "password": password}


        response = requests.post(str(azure + "account/login"),
                                    json=payload,verify = False)
        if response.status_code == 200:
            global auth_token
            auth_token = response.json()['token']

            try:
                role = response.json()['userDto']['role']['name']
                if role == 'Admin':
                    AdminPanel()
                elif role =='Worker':
                    WorkerPanel()
                else:
                    UserPanel()
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
if unresizable:
    window.resizable(width=0, height=0)
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

login_button = tk.Button(window,text="Login", command=login)
login_button.grid(row=3, column=0, sticky="E", padx=200)
register_button = tk.Button(window,text="Register", command=register)
register_button.grid(row=4, column=0, sticky="E", padx=200)
login_button.config(width=100, height=1)
register_button.config(width=100, height=1)

# endregion


if __name__ == "__main__":
    window.mainloop()






