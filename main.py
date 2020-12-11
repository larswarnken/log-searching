from tkinter import *
from tkinter import filedialog
import os
from tkinter import ttk
import json

# getting directory


# set up window
root = Tk()
root.title("search logs")
root.configure(bg="#424242")


def set_dir():
    root.filename = filedialog.askdirectory()
    print(root.filename)

    with open('directory.json', 'w') as f:
        json.dump(str(root.filename), f)

    return str(root.filename)


def get_dir():
    with open('directory.json') as f:
        data = json.load(f)
    print(data)


channel = StringVar()
channel_chosen = ttk.Combobox(root, width=25, textvariable=channel)

# Adding combobox drop down list
channel_chosen['values'] = (' January',
                            ' February',
                            ' March',
                            ' April',
                            ' May',
                            ' June',
                            ' July',
                            ' August',
                            ' September',
                            ' October',
                            ' November',
                            ' December')

# labels
label_channel = Label(root, text="Channel: ", bg="#424242", fg="white")

# buttons
button_dir = Button(root, text="set directory", command=lambda: set_dir())
button_get_dir = Button(root, text="get directory", command=lambda: get_dir())

# grid
label_channel.grid(row=0, column=0)
channel_chosen.grid(row=0, column=1)
button_dir.grid(row=0, column=10)
button_get_dir.grid(row=0, column=11)

root.mainloop()
