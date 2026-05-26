danh_sach_hex = input("Dán đoạn mã nhị phân vào đây: ")
danh_sach_hex = chuoi_hex.split()
tin_goc = ""
for h in danh_sach_hex:
    # Chuyển hệ 16 -> số -> chữ cái
    chu_cai = chr(int(h, 16))
    tin_goc += chu_cai
    
print(f"\n--- Đang giải mã... ---")
time.sleep(1)
print(f"Tin nhắn gốc: {tin_goc}")
