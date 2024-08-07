import tkinter as tk
from tkinter import Menu, Text, Scrollbar, N, E, S, W, RIGHT, Y, END
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import colorchooser
import os

class Notepad:
    def __init__(self, **kwargs):
        # Initialize root window
        self.root = tk.Tk()

        # Set window dimensions
        self.width = kwargs.get('width', 300)
        self.height = kwargs.get('height', 300)

        # Set the window title and icon
        self.root.title("Untitled - Notepad")
        try:
            self.root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        left = (screen_width // 2) - (self.width // 2)
        top = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f'{self.width}x{self.height}+{left}+{top}')

        # Configure grid for auto-resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Text area and scrollbar
        self.text_area = Text(self.root)
        self.scroll_bar = Scrollbar(self.text_area)
        self.text_area.grid(sticky=N+E+S+W)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.scroll_bar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)

        # Menu bar
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.format_menu = Menu(self.menu_bar, tearoff=0)  # New Format menu

        # File menu options
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit_application)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu options
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Format menu options
        self.format_menu.add_command(label="Font Color", command=self.change_color)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)

        # Help menu options
        self.help_menu.add_command(label="About Notepad", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Set menu bar
        self.root.config(menu=self.menu_bar)

        # File path variable
        self.file = None

    def quit_application(self):
        self.root.destroy()

    def show_about(self):
        showinfo("Notepad", "Notepad by Mrinal Verma")

    def open_file(self):
        self.file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file:
            self.root.title(f"{os.path.basename(self.file)} - Notepad")
            self.text_area.delete(1.0, END)
            with open(self.file, "r") as file:
                self.text_area.insert(1.0, file.read())

    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(1.0, END)

    def save_file(self):
        if self.file is None:
            self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file:
            with open(self.file, "w") as file:
                file.write(self.text_area.get(1.0, END))
            self.root.title(f"{os.path.basename(self.file)} - Notepad")

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def change_color(self):
        # Open color chooser dialog
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            try:
                self.text_area.tag_add("colored", "sel.first", "sel.last")
                self.text_area.tag_config("colored", foreground=color)
            except tk.TclError:
                showinfo("Notepad", "Please select text to change color.")

    def run(self):
        self.root.mainloop()

# Run main application
if __name__ == "__main__":
    notepad = Notepad(width=600, height=400)
    notepad.run()
