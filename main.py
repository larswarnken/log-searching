import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import os.path
from tkinter import ttk
import json
import tkinter.scrolledtext as tkst


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


# get search key
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


# dropdown style
combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings={'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'grey',
                                       'fieldbackground': '#424242',
                                       'background': '#424242',
                                       'foreground': 'white'
                                       }}}
                         )

combostyle.theme_use('combostyle')


##################################################################################################################


# dropdown menu
channel = tk.StringVar()
channel_chosen = ttk.Combobox(root, width=15, textvariable=channel)
channel_chosen['values'] = get_folders()

# labels
label_channel = tk.Label(root, text="Channel: ", bg="#424242", fg="white")
label_search = tk.Label(root, text="Search: ", bg="#424242", fg="white")
label_logs_found = tk.Label(root, text="xx.xxx logs found since xx-xx-xxxx", bg="#424242", fg="white")
label_macthes_found = tk.Label(root, text="xxx.xxx matches", bg="#424242", fg="white")
label_placeholder1 = tk.Label(root, text="", bg="#424242")
label_placeholder2 = tk.Label(root, text="", bg="#424242")

# buttons
button_dir = tk.Button(root, text="change directory", command=lambda: set_dir(), fg="white", bg="#424242")
button_search = tk.Button(root, text="search", width=8, command=lambda: get_search_key(), fg="white", bg="#424242")
button_messages = tk.Button(root, text="messages", width=8, command=lambda: get_search_key(), fg="white", bg="#424242")
button_mentions = tk.Button(root, text="mentions", width=8, command=lambda: get_search_key(), fg="white", bg="#424242")

# text entries
search_entry = tk.Entry(root, width=17, bg="#424242", fg="white")

# dings
editArea = tkst.ScrolledText(master=root, wrap=WORD, width=120, height=30, font=("Calibri", 11), bg="#424242", fg="white")


# grid
label_channel.grid(row=0, column=0, sticky=W, padx=5, pady=5)
channel_chosen.grid(row=0, column=1, sticky=W, padx=5, pady=5)
label_logs_found.grid(row=0, column=2, columnspan=3, padx=5, pady=5)
label_placeholder1.grid(row=0, column=5, padx=5, pady=5)
button_dir.grid(row=0, column=6, padx=5, pady=5)

label_search.grid(row=1, column=0, sticky=W, padx=5, pady=5)
search_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
button_search.grid(row=1, column=2, padx=5, pady=5)
button_messages.grid(row=1, column=3, padx=5, pady=5)
button_mentions.grid(row=1, column=4, padx=5, pady=5)
label_placeholder1.grid(row=1, column=5, padx=5, pady=5)
label_macthes_found.grid(row=1, column=6, padx=5, pady=5)

editArea.grid(row=2, column=0, columnspan=7, sticky=N+E+S+W)

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(5, weight=1)
root.grid_rowconfigure(2, weight=1)


# for return key
search_entry.bind("<Return>", (lambda event: get_search_key()))

root.mainloop()
