from tkinter import *
from tkinter import ttk


class FeetToMeters:
    def __init__(self, root):
        root.title("Feet To Meters")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet = StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))

        self.meters = StringVar()

        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Enter>", self.calculate)

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
        except ValueError:
            pass


"""
root = Tk()
FeetToMeters(root)
root.mainloop()
"""


def get_username(*args):
    print(*args)
    name = username.get()
    getusername.set(name)


if __name__ == "__main__":
    root = Tk()

    mainframe = ttk.Frame(root, padding="100 50 100 50")
    mainframe.grid(column=0, row=1, sticky='nwes')
    ttk.Label(mainframe, text="hello").grid(column=1, row=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    phone = StringVar()
    home = ttk.Radiobutton(mainframe, text='Home', variable=phone, value='home')
    home.grid(column=1, row=2)

    username = StringVar()
    name = ttk.Entry(mainframe, textvariable=username, show="*")
    name.grid(column=3, row=3)
    username_label = ttk.Label(mainframe, text="username: ")
    username_label.grid(column=2, row=3)

    getusername = StringVar()
    show_username = ttk.Label(mainframe, textvariable=getusername)
    show_username.grid(column=4, row=2)
    ttk.Label(mainframe, text="show").grid(column=3, row=2)

    button = ttk.Button(mainframe, text="get", command=get_username)
    button.grid(column=4, row=3)

    country = ttk.Combobox(mainframe)
    country.grid(column=5, row=3)
    country['values'] = ('USA', 'PRC', 'Canada')
    root.bind("<Enter>", get_username)

    otherframe = ttk.Frame(root, padding="100 1 1 100")
    otherframe.grid(column=1, row=1)
    ttk.Label(otherframe, text="hello hello").grid(column=1, row=1)
    root.mainloop()
