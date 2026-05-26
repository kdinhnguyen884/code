tin_nhan = input("\nNhập tin nhắn cần mã hóa sang Hệ 16: ")
ket_qua = []
for chu in tin_nhan:
    # Chuyển chữ -> số -> hệ 16 (bỏ '0x')
    ma_hex = hex(ord(chu))[2:].upper() 
    ket_qua.append(ma_hex)
    
chuoi_hex = " ".join(ket_qua)
print(f"--- Đang mã hóa... ---")
time.sleep(1) # Tạo hiệu ứng chờ cho ngầu
print(f"Kết quả Hex: {chuoi_hex}")
