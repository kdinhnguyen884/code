import random

# 1. Tạo file dữ liệu mẫu
with open("SỐ.INP", "w", encoding="utf-8") as f:
    a = random.randint(1, 10**6) # Để nhỏ lại chút cho dễ kiểm tra
    f.write(str(a))

# 2. Đọc file
with open("SỐ.INP", "r") as f:
    noidung = f.read().strip()
    if noidung:
        n = int(noidung)
    else:
        n = 0

# 3. Hàm kiểm tra
def la_doi_xung(n):
    s = str(n)
    return s == s[::-1]

def tong_la_chan(n):
    # Cách tính tổng các chữ số: Chuyển sang chuỗi rồi sang int từng số
    s = sum(int(chuso) for chuso in str(n))
    return s % 2 == 0

# 4. Kiểm tra điều kiện và ghi file
# Ta lấy n làm tham số truyền vào các hàm
if la_doi_xung(n) and tong_la_chan(n):
    ket_qua = "YES"
else:
    ket_qua = "NO"

with open("SỐ.OUT", "w") as f:
    f.write(ket_qua)

print(f"Số vừa kiểm tra: {n}")
print(f"Kết quả: {ket_qua}")
