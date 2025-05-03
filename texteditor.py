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
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.button_frame = Frame(self.root, bg="#2E2E2E")
        self.button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        self.add_font_menu()
        self.add_file_buttons()
        self.add_find_replace_button()
        self.add_dark_mode_button()
        self.add_word_count_label()

        # Creating the Text Widget
        self.text = Text(self.root, wrap="word", font=("Helvetica", 12), undo=True, bg="#FFFFFF", fg="#000000")
        self.text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.autosave()
        self.text.bind("<KeyRelease>", self.update_word_count)

    def add_font_menu(self):
        font_menu = Menubutton(self.button_frame, text="Font", relief=RAISED, bg="#4B4B4B", fg="white")
        font_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        font_menu.menu = Menu(font_menu, tearoff=0)
        font_menu["menu"] = font_menu.menu

        helvetica = IntVar()
        courier = IntVar()
        font_menu.menu.add_checkbutton(label="Courier", variable=courier, command=self.set_font_courier)
        font_menu.menu.add_checkbutton(label="Helvetica", variable=helvetica, command=self.set_font_helvetica)

    def set_font_helvetica(self):
        self.text.config(font=("Helvetica", 12))

    def set_font_courier(self):
        self.text.config(font=("Courier", 12))

    def add_file_buttons(self):
        save_button = self.create_button(self.button_frame, "Save", self.save_file, 1)
        open_button = self.create_button(self.button_frame, "Open", self.open_file, 2)

    def create_button(self, parent, text, command, column):
        button = Button(parent, text=text, command=command, bg="#56B5D8", fg="white", relief=FLAT, font=("Helvetica", 10))
        button.grid(row=0, column=column, padx=5, pady=5, sticky="w")
        button.bind("<Enter>", lambda e: button.config(bg="#4595B8"))
        button.bind("<Leave>", lambda e: button.config(bg="#56B5D8"))
        return button

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
        find_button = self.create_button(self.button_frame, "Find/Replace", self.find_and_replace, 3)

    def find_and_replace(self):
        find_window = Toplevel(self.root)
        find_window.title("Find and Replace")
        find_window.configure(bg="#2E2E2E")

        Label(find_window, text="Find:", bg="#2E2E2E", fg="white").grid(row=0, column=0, padx=5, pady=5)
        find_entry = Entry(find_window)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(find_window, text="Replace:", bg="#2E2E2E", fg="white").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = Entry(find_window)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        def replace_text():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text.get("1.0", "end")
            new_content = content.replace(find_text, replace_text)
            self.text.delete("1.0", "end")
            self.text.insert("1.0", new_content)

        Button(find_window, text="Replace", command=replace_text, bg="#56B5D8", fg="white", relief=FLAT, font=("Helvetica", 10)).grid(row=2, column=0, columnspan=2, pady=5)

    def add_dark_mode_button(self):
        dark_mode_button = self.create_button(self.button_frame, "Dark Mode", self.toggle_dark_mode, 4)

    def toggle_dark_mode(self):
        current_bg = self.text.cget("bg")
        if current_bg == "#FFFFFF":
            self.text.config(bg="#2E2E2E", fg="#FFFFFF", insertbackground="white")
            self.button_frame.config(bg="#2E2E2E")
            for widget in self.button_frame.winfo_children():
                widget.config(bg="#4B4B4B", fg="white")
        else:
            self.text.config(bg="#FFFFFF", fg="#000000", insertbackground="black")
            self.button_frame.config(bg="#2E2E2E")
            for widget in self.button_frame.winfo_children():
                widget.config(bg="#56B5D8", fg="white")

    def add_word_count_label(self):
        self.word_count_label = Label(self.button_frame, text="Words: 0", bg="#2E2E2E", fg="white")
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
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    app = TextEditor(root)
    root.mainloop()