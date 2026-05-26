import customtkinter as ctk
import sqlite3
from datetime import datetime
from tkinter import messagebox
import os
import sys

# --- HÀM HỖ TRỢ ĐƯỜNG DẪN (QUAN TRỌNG ĐỂ ĐÓNG GÓI) ---
def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối đến tài nguyên, hỗ trợ cả khi chạy file .py và .exe """
    try:
        # PyInstaller tạo một thư mục tạm và lưu trữ đường dẫn trong _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- PHẦN 1: DATABASE ---
class FinanceProDB:
    def __init__(self):
        # Sử dụng resource_path để xác định vị trí file database
        db_path = resource_path("finance_pro.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                              (id INTEGER PRIMARY KEY, amount REAL, type TEXT, category TEXT, date TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, current_balance REAL)''')
        
        self.cursor.execute("SELECT COUNT(*) FROM balance")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO balance (current_balance) VALUES (0)")
        self.conn.commit()

    def add_transaction(self, amount, t_type, category):
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cursor.execute("INSERT INTO transactions (amount, type, category, date) VALUES (?, ?, ?, ?)", 
                           (amount, t_type, category, date_str))
        
        if t_type == "Thu nhập":
            self.cursor.execute("UPDATE balance SET current_balance = current_balance + ?", (amount,))
        else:
            self.cursor.execute("UPDATE balance SET current_balance = current_balance - ?", (amount,))
        self.conn.commit()

    def clear_all_history(self):
        self.cursor.execute("DELETE FROM transactions")
        self.cursor.execute("UPDATE balance SET current_balance = 0")
        self.conn.commit()

    def get_data(self):
        self.cursor.execute("SELECT current_balance FROM balance WHERE id = 1")
        result = self.cursor.fetchone()
        balance = result[0] if result else 0
        self.cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
        history = self.cursor.fetchall()
        return balance, history

# --- PHẦN 2: GIAO DIỆN ---
class FinanceProApp:
    def __init__(self, root):
        self.db = FinanceProDB()
        self.root = root
        self.root.title("Finance Tracker Pro Max")
        self.root.geometry("550x750")
        ctk.set_appearance_mode("dark")

        # UI Components
        self.balance_label = ctk.CTkLabel(root, text="SỐ DƯ: 0 VNĐ", font=("Arial", 26, "bold"))
        self.balance_label.pack(pady=20)

        self.input_frame = ctk.CTkFrame(root)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.amount_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Nhập số tiền...", width=200)
        self.amount_entry.grid(row=0, column=0, padx=10, pady=10)

        self.cat_menu = ctk.CTkComboBox(self.input_frame, values=["Lương", "Ăn uống", "Shopping", "Học tập", "Di chuyển", "Khác"])
        self.cat_menu.grid(row=0, column=1, padx=10, pady=10)

        self.inc_btn = ctk.CTkButton(self.input_frame, text="+ THU NHẬP", fg_color="#2ecc71", command=lambda: self.process("Thu nhập"))
        self.inc_btn.grid(row=1, column=0, padx=10, pady=10)

        self.exp_btn = ctk.CTkButton(self.input_frame, text="- CHI TIÊU", fg_color="#e74c3c", command=lambda: self.process("Chi tiêu"))
        self.exp_btn.grid(row=1, column=1, padx=10, pady=10)

        self.clear_btn = ctk.CTkButton(root, text="DỌN DẸP TOÀN BỘ LỊCH SỬ", fg_color="transparent", 
                                        border_width=1, text_color="#e74c3c", command=self.confirm_clear)
        self.clear_btn.pack(pady=5)

        self.history_frame = ctk.CTkScrollableFrame(root, width=500, height=350, label_text="Lịch sử dòng tiền")
        self.history_frame.pack(pady=20)

        self.refresh_display()

    def process(self, t_type):
        try:
            val = float(self.amount_entry.get())
            cat = self.cat_menu.get()
            self.db.add_transaction(val, t_type, cat)
            self.amount_entry.delete(0, 'end')
            self.refresh_display()
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập số tiền hợp lệ!")

    def confirm_clear(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ lịch sử và đưa số dư về 0 không?"):
            self.db.clear_all_history()
            self.refresh_display()

    def refresh_display(self):
        balance, history = self.db.get_data()
        color = "#2ecc71" if balance >= 0 else "#e74c3c"
        self.balance_label.configure(text=f"SỐ DƯ: {balance:,.0f} VNĐ", text_color=color)

        for widget in self.history_frame.winfo_children():
            widget.destroy()

        for _, amt, t_type, cat, date in history:
            row = ctk.CTkFrame(self.history_frame)
            row.pack(fill="x", pady=3, padx=5)
            
            st_color = "#2ecc71" if t_type == "Thu nhập" else "#e74c3c"
            status_label = ctk.CTkLabel(row, text=t_type.upper(), text_color="white", 
                                         fg_color=st_color, corner_radius=6, width=85, font=("Arial", 10, "bold"))
            status_label.pack(side="left", padx=10)

            ctk.CTkLabel(row, text=f"{date} | {cat}").pack(side="left")
            symbol = "+" if t_type == "Thu nhập" else "-"
            ctk.CTkLabel(row, text=f"{symbol}{amt:,.0f}", text_color=st_color, font=("Arial", 13, "bold")).pack(side="right", padx=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = FinanceProApp(root)
    root.mainloop()
