import sys
if sys.version_info[0] < 3:
    from Tkinter import *
    import tkFileDialog as filedialog
else:
    from tkinter import *
    from tkinter import filedialog
    from tkinter import messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Quill")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.text = Text(self.root, wrap="word", font="Helvetica", undo=True)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=1, column=0, sticky="ew")
        self.add_font_menu()
        self.add_file_buttons()
        self.add_find_replace_button()
        self.add_dark_mode_button()
        self.add_word_count_label()
        self.autosave()
        self.text.bind("<KeyRelease>", self.update_word_count)

    def add_font_menu(self):
        font_menu = Menubutton(self.button_frame, text="Font", relief=RAISED, bg="black", fg="white")
        font_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        font_menu.menu = Menu(font_menu, tearoff=0)
        font_menu["menu"] = font_menu.menu
        helvetica = IntVar()
        courier = IntVar()
        font_menu.menu.add_checkbutton(label="Courier", variable=courier, command=self.set_font_courier)
        font_menu.menu.add_checkbutton(label="Helvetica", variable=helvetica, command=self.set_font_helvetica)

    def set_font_helvetica(self):
        self.text.config(font="Helvetica")

    def set_font_courier(self):
        self.text.config(font="Courier")

    def add_file_buttons(self):
        save_button = Button(self.button_frame, text="Save", command=self.save_file, bg="black", fg="white")
        save_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        open_button = Button(self.button_frame, text="Open", command=self.open_file, bg="black", fg="white")
        open_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    def save_file(self):
        try:
            content = self.text.get("1.0", "end-1c")
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text Files", "*.txt"),
                                                                ("All Files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file:\n{e}")

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text.delete("1.0", "end")
                self.text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file:\n{e}")

    def add_find_replace_button(self):
        find_button = Button(self.button_frame, text="Find/Replace", command=self.find_and_replace, bg="black", fg="white")
        find_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    def find_and_replace(self):
        find_window = Toplevel(self.root)
        find_window.title("Find and Replace")
        Label(find_window, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = Entry(find_window)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        Label(find_window, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = Entry(find_window)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        def replace_text():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text.get("1.0", "end")
            new_content = content.replace(find_text, replace_text)
            self.text.delete("1.0", "end")
            self.text.insert("1.0", new_content)
        Button(find_window, text="Replace", command=replace_text).grid(row=2, column=0, columnspan=2, pady=5)

    def add_dark_mode_button(self):
        dark_mode_button = Button(self.button_frame, text="Dark Mode", command=self.toggle_dark_mode, bg="black", fg="white")
        dark_mode_button.grid(row=0, column=4, padx=5, pady=5, sticky="w")

    def toggle_dark_mode(self):
        current_bg = self.text.cget("bg")
        if current_bg == "white":
            self.text.config(bg="black", fg="white", insertbackground="white")
        else:
            self.text.config(bg="white", fg="black", insertbackground="black")

    def add_word_count_label(self):
        self.word_count_label = Label(self.button_frame, text="Words: 0", bg="black", fg="white")
        self.word_count_label.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    def update_word_count(self, event=None):
        content = self.text.get("1.0", "end-1c")
        word_count = len(content.split())
        self.word_count_label.config(text=f"Words: {word_count}")

    def autosave(self):
        content = self.text.get("1.0", "end-1c")
        with open("autosave.txt", "w") as file:
            file.write(content)
        self.root.after(300000, self.autosave)

if __name__ == "__main__":
    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = TextEditor(root)
    root.mainloop()