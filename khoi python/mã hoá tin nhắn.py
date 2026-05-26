tin_nhan = input("Nhập tin nhắn: ")
khoa = int(input("Nhập số khóa: "))
tin_ma_hoa = ""

for chu in tin_nhan:
    # ord(chu) + khoa: tính mã số mới
    # bin(...)[2:]: chuyển sang nhị phân và bỏ chữ '0b'
    # .zfill(8): đảm bảo mỗi chữ cái luôn có 8 ký tự (tùy chọn)
    chu_nhiphun = bin(ord(chu) + khoa)[2:]
    tin_ma_hoa += chu_nhiphun + " " # Thêm khoảng cách để dễ đọc

print(f"Tin nhắn bí mật (Nhị phân): {tin_ma_hoa}")
