import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# --- PHẦN 1: QUẢN LÝ DATABASE (SQLite) ---
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("todo_pro.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                              (id INTEGER PRIMARY KEY, ten TEXT, hoan_thanh INTEGER)''')
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def add_task(self, name):
        self.cursor.execute("INSERT INTO tasks (ten, hoan_thanh) VALUES (?, 0)", (name,))
        self.conn.commit()

    def update_task(self, task_id, status):
        self.cursor.execute("UPDATE tasks SET hoan_thanh = ? WHERE id = ?", (status, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

# --- PHẦN 2: GIAO DIỆN (CustomTkinter) ---
class TodoProApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Todo List Pro 2026")
        self.root.geometry("500x550")
        ctk.set_appearance_mode("dark") # Chế độ tối

        # Tiêu đề
        self.label = ctk.CTkLabel(root, text="DANH SÁCH CÔNG VIỆC", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # Khung nhập liệu
        self.entry = ctk.CTkEntry(root, placeholder_text="Bạn cần làm gì hôm nay?", width=350)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda e: self.add_task()) # Phím Enter 

        self.add_btn = ctk.CTkButton(root, text="THÊM", command=self.add_task, fg_color="#2ecc71")
        self.add_btn.pack(pady=5)

        # Danh sách hiển thị (Scrollable Frame)
        self.scroll_frame = ctk.CTkScrollableFrame(root, width=400, height=250)
        self.scroll_frame.pack(pady=20)

        self.refresh_list()

    def refresh_list(self):
        # Xóa các widget cũ trong frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks()
        for task_id, name, done in tasks:
            status = " [DONE]" if done else ""
            color = "#7f8c8d" if done else "#ffffff"
            
            # Tạo một dòng công việc với nút xóa bên cạnh
            f = ctk.CTkFrame(self.scroll_frame)
            f.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(f, text=f"{name}{status}", text_color=color)
            lbl.pack(side="left", padx=10)

            # Nút đánh dấu xong
            if not done:
                done_btn = ctk.CTkButton(f, text="✔", width=30, command=lambda i=task_id: self.mark_done(i))
                done_btn.pack(side="right", padx=5)
            
            # Nút xóa
            del_btn = ctk.CTkButton(f, text="X", width=30, fg_color="#e74c3c", command=lambda i=task_id: self.delete_task(i))
            del_btn.pack(side="right")

    def add_task(self):
        name = self.entry.get()
        if name:
            self.db.add_task(name)
            self.entry.delete(0, 'end')
            self.refresh_list()

    def mark_done(self, task_id):
        self.db.update_task(task_id, 1)
        self.refresh_list()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh_list()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoProApp(root)
    root.mainloop()
