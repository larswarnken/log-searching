import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import os.path
from pathlib import Path
from tkinter import ttk
import json
import tkinter.scrolledtext as tkst
import re
import glob


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
        return search_entry.get()


# when an option from dropdown is clicked
def dropdown_selected(event):
    dropdown_text = channel_chosen.get()
    if dropdown_text in found_channels:
        if channel_chosen.get() != 'mentions':
            count = len(os.listdir(path=str(f'{log_dir}\\Channels\\{dropdown_text}')))
            first_date_name = sorted(os.listdir(path=str(f'{log_dir}\\Channels\\{dropdown_text}')))[0]
        else:
            count = len(os.listdir(path=str(f'{log_dir}\\{dropdown_text}')))
            first_date_name = sorted(os.listdir(path=str(f'{log_dir}\\{dropdown_text}')))[0]

        label_logs_found['text'] = f'{count} logs found since {log_name_to_date(first_date_name)}'
    else:
        label_logs_found['text'] = 'no logs found'


# extracts date out of log file name
def log_name_to_date(long_name):
    matches = re.findall(r'(?:\d+)', long_name)
    return f'{matches[-1]}-{matches[-2]}-{matches[-3]}'


# shows every chatline with search key in it
def general_search(key):
    if key != "":
        file_search(key)


def messages_search(key):
    if key != "":
        modified_key = f']  {key}:'
        file_search(modified_key)


def mentions_search(key):
    if key != "":
        editArea.delete('1.0', END)
        message_counter = 0
        results = []
        for file in os.listdir(path=str(f'{log_dir}\\Channels\\{channel_chosen.get()}')):
            file_path = f'{log_dir}\\Channels\\{channel_chosen.get()}\\{file}'
            with open(file_path, 'r', encoding="utf8", errors='ignore') as log:
                all_messages_from_log = log.read().split("\n")
            for line in all_messages_from_log:
                if key in line and str(f'{key}: ') not in line:
                    message_counter += 1
                    results.append(f'{log_name_to_date(file)} {line}')
        results.reverse()
        label_macthes_found['text'] = f'{format(message_counter, ",d")} matches'
        if message_counter == 0:
            result_string = 'no matches lol'
            editArea.insert(INSERT, str(result_string))
        else:
            result_string = '\n'.join(results)
            editArea.insert(INSERT, str(result_string))


# searches in all files for key
def file_search(key):
    editArea.delete('1.0', END)
    message_counter = 0
    results = []
    for file in os.listdir(path=str(f'{log_dir}\\Channels\\{channel_chosen.get()}')):
        file_path = f'{log_dir}\\Channels\\{channel_chosen.get()}\\{file}'
        with open(file_path, 'r', encoding="utf8", errors='ignore') as log:
            all_messages_from_log = log.read().split("\n")
        for line in all_messages_from_log:
            if key in line:
                message_counter += 1
                results.append(f'{log_name_to_date(file)} {line}')
    results.reverse()
    label_macthes_found['text'] = f'{format(message_counter, ",d")} matches'
    if message_counter == 0:
        result_string = 'no matches lol'
        editArea.insert(INSERT, str(result_string))
    else:
        result_string = '\n'.join(results)
        editArea.insert(INSERT, str(result_string))



##################################################################################################################


# checking if dir json file exists, else creating default file
if not os.path.isfile("directory.json"):
    with open('directory.json', 'w') as f:
        json.dump(str(os.getenv('APPDATA') + "\\Chatterino2\\Logs\\Twitch"), f)


# setting log dir
log_dir = get_dir()

# all found channels
found_channels = get_folders()


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
channel_chosen['values'] = found_channels
channel_chosen.bind("<<ComboboxSelected>>", dropdown_selected)

# labels
label_channel = tk.Label(root, text="Channel: ", bg="#424242", fg="white")
label_search = tk.Label(root, text="Search: ", bg="#424242", fg="white")
label_logs_found = tk.Label(root, text="", bg="#424242", fg="white")
label_macthes_found = tk.Label(root, text="", bg="#424242", fg="white")
label_placeholder1 = tk.Label(root, text="", bg="#424242")
label_placeholder2 = tk.Label(root, text="", bg="#424242")

# buttons
button_dir = tk.Button(root, text="change directory", command=lambda: set_dir(), fg="white", bg="#424242")
button_search = tk.Button(root, text="search", width=8, command=lambda: general_search(str(get_search_key())), fg="white", bg="#424242")
button_messages = tk.Button(root, text="messages", width=8, command=lambda: messages_search(str(get_search_key())), fg="white", bg="#424242")
button_mentions = tk.Button(root, text="mentions", width=8, command=lambda: mentions_search(str(get_search_key())), fg="white", bg="#424242")

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
channel_chosen.bind("<Return>", lambda event: dropdown_selected(None))
search_entry.bind("<Return>", lambda event: general_search(str(get_search_key())))

root.mainloop()


# TODO: save last channel



