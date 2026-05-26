r = int(input("Nhập lượng màu Đỏ (0-255): "))
g = int(input("Nhập lượng màu Xanh lá (0-255): "))
b = int(input("Nhập lượng màu Xanh dương (0-255): "))

# Chuyển từng số sang hệ 16, bỏ '0x', và đảm bảo có 2 chữ số (zfill)
hex_r = hex(r)[2:].zfill(2).upper()
hex_g = hex(g)[2:].zfill(2).upper()
hex_b = hex(b)[2:].zfill(2).upper()

ma_mau = "#" + hex_r + hex_g + hex_b

print(f"Mã màu Hệ 16 của bạn là: {ma_mau}")
