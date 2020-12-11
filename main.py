import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import os.path
from tkinter import ttk
import json


# set directory of logs trough explorer
def set_dir():
    tk.messagebox.showinfo(title="Log Directory",
                           message="select your chatterino log folder, e.g.: "
                                   "\"C:/.../Chatterino2/Logs/Twitch\"")

    root.filename = filedialog.askdirectory()

    if root.filename != "":
        with open('directory.json', 'w') as f:
            json.dump(str(root.filename), f)

        return str(root.filename)
    else:
        return get_dir()


# get the saved directory from json file
def get_dir():
    with open('directory.json') as f:
        log_dir_json = json.load(f)
    print(log_dir_json)
    return log_dir_json


# get all log folders within log dir
def get_folders():
    folders = os.listdir(path=log_dir)
    channels = os.listdir(path=str(log_dir + "\\Channels"))

    channels.sort()

    if "Mentions" in folders:
        channels.insert(0, 'mentions')

    return channels


def get_search_key():
    if search_entry.get() != "":
        print(search_entry.get())


##################################################################################################################


# checking if dir json file exists, else creating default file
if not os.path.isfile("directory.json"):
    with open('directory.json', 'w') as f:
        json.dump(str(os.getenv('APPDATA') + "\\Chatterino2\\Logs\\Twitch"), f)


# setting log dir
log_dir = get_dir()


# set up window
root = tk.Tk()
root.title("search logs")
root.configure(bg="#424242")


##################################################################################################################


# dropdown menu
channel = tk.StringVar()
channel_chosen = ttk.Combobox(root, width=15, textvariable=channel)
channel_chosen['values'] = get_folders()

# labels
label_channel = tk.Label(root, text="Channel: ", bg="#424242", fg="white")
label_search = tk.Label(root, text="Search: ", bg="#424242", fg="white")

# buttons
button_dir = tk.Button(root, text="change directory", command=lambda: set_dir())
button_get_dir = tk.Button(root, text="get directory", command=lambda: get_dir())
button_get_folders = tk.Button(root, text="get folders", command=lambda: print(get_folders()))
button_search = tk.Button(root, text="search", command=lambda:get_search_key())

# text entries
search_entry = tk.Entry(root, width=18)

# grid
label_channel.grid(row=0, column=10)
channel_chosen.grid(row=0, column=20)
button_dir.grid(row=0, column=30)
button_get_dir.grid(row=0, column=40)
button_get_folders.grid(row=0, column=50)

label_search.grid(row=10, column=10)
search_entry.grid(row=10, column=20)
button_search.grid(row=10, column=30)


# for return key
# search_entry.bind("<Return>", (lambda event: general_search(search_entry.get())))

root.mainloop()
