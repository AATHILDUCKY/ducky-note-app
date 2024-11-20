import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note-Taking App")
        self.root.geometry("1050x700")
        self.root.configure(bg="#FFA500")  # Orange theme

        # SQLite database setup
        self.conn = sqlite3.connect("notes.db")
        self.create_table()

        # Top Navigation
        self.nav_frame = ttk.Frame(self.root, style="NavFrame.TFrame")
        self.nav_frame.pack(side="top", fill="x", pady=10)

        style = ttk.Style()
        style.configure("NavButton.TButton", font=("Arial", 12, "bold"), padding=10, background="#FFA500")
        style.map("NavButton.TButton", background=[("active", "#FF8C00")])

        self.search_btn = ttk.Button(self.nav_frame, text="Search Notes", command=self.show_search_section, style="NavButton.TButton")
        self.search_btn.pack(side="left", padx=20)

        self.insert_btn = ttk.Button(self.nav_frame, text="Insert Notes", command=self.show_insert_section, style="NavButton.TButton")
        self.insert_btn.pack(side="left", padx=20)


        # Content Section
        self.content_frame = ttk.Frame(self.root, style="ContentFrame.TFrame")
        self.content_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("ContentFrame.TFrame", background="#FFD580")  # Light orange theme

        self.show_search_section()


    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                keywords TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def show_insert_section(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.content_frame, text="Title:", font=("Arial", 14), background="#FFD580", foreground="black").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = ttk.Entry(self.content_frame, width=80)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.content_frame, text="Keywords (comma-separated):", font=("Arial", 14), background="#FFD580", foreground="black").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.keywords_entry = ttk.Entry(self.content_frame, width=80)
        self.keywords_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.content_frame, text="Content:", font=("Arial", 14), background="#FFD580", foreground="black").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        self.content_text = tk.Text(self.content_frame, width=80, height=20, font=("Consolas", 12))
        self.content_text.grid(row=2, column=1, padx=10, pady=10)

        self.insert_btn = ttk.Button(self.content_frame, text="Insert Note", command=self.insert_note, style="InsertButton.TButton")
        style = ttk.Style()
        style.configure("InsertButton.TButton", font=("Arial", 14, "bold"), padding=10, background="#FFA500")
        style.map("InsertButton.TButton", background=[("active", "#FF8C00")])
        self.insert_btn.grid(row=3, column=1, padx=10, pady=20, sticky="e")


    def insert_note(self):
        title = self.title_entry.get().strip()
        keywords = self.keywords_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not title or not keywords or not content:
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO notes (title, keywords, content) VALUES (?, ?, ?)", (title, keywords, content))
        self.conn.commit()
        messagebox.showinfo("Success", "Note inserted successfully!")
        self.title_entry.delete(0, tk.END)
        self.keywords_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def show_search_section(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.content_frame, text="Search Keywords (comma-separated):", background="#FFA500",foreground="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_entry = ttk.Entry(self.content_frame, width=80)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_notes)

        self.results_frame = ttk.Frame(self.content_frame)
        self.results_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    
    def search_notes(self, event=None):
        keywords = self.search_entry.get().strip()
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not keywords:
            return

        keywords_list = [kw.strip().lower() for kw in keywords.split(",")]
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, content, keywords FROM notes")
        results = cursor.fetchall()

        for note_id, title, content, note_keywords in results:
            note_keywords_list = [kw.strip().lower() for kw in note_keywords.split(",")]
        
            # Check for partial matches
            if all(any(kw in db_kw for db_kw in note_keywords_list) for kw in keywords_list):
                self.display_result(note_id, title, content)

    def display_result(self, note_id, title, content):
        result_frame = ttk.Frame(self.results_frame, relief="solid", borderwidth=1)
        result_frame.pack(fill="x", padx=5, pady=5, expand=True)

        ttk.Label(result_frame, text=title, font=("Arial", 14, "bold"), background="white").pack(
            side="top", anchor="w", padx=5, pady=5)
        content_text = tk.Text(result_frame, height=10,wrap="word", font=("Consolas", 12), background="#FFF8DC", borderwidth=0)
        content_text.insert("1.0", content)
        content_text.configure(state="disabled")
        content_text.pack(fill="x", padx=5, pady=5)

        # Delete Button
        delete_button = ttk.Button(result_frame, text="Delete", command=lambda: self.delete_note(note_id, result_frame))
        delete_button.pack(side="bottom", anchor="e", padx=5, pady=5)

    def delete_note(self, note_id, result_frame):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
        if confirm:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Note deleted successfully!")
            result_frame.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
