# Bước 1: Tạo bộ từ điển của bạn
tu_dien = {
    "hello": "xin chào",
    "cat": "con mèo",
    "dog": "con chó",
    "apple": "quả táo"
}

# Bước 2: Cho người dùng nhập từ muốn tra
tu_can_tra = input("Nhập từ tiếng Anh bạn muốn dịch: ")

# Bước 3: Kiểm tra xem từ đó có trong từ điển không
if tu_can_tra in tu_dien:
    print(f"Nghĩa của nó là: {tu_dien[tu_can_tra]}")
else:
    print("Xin lỗi, từ này mình chưa học!")
