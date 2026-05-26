tin_nhan_nhan_duoc = input("Dán đoạn mã nhị phân vào đây: ")
khoa_giai_ma = int(input("Nhập số khóa bí mật: "))

danh_sach_nhi_phan = tin_nhan_nhan_duoc.split()
tin_goc = ""

for nhi_phan in danh_sach_nhi_phan:
    # 1. Chuyển nhị phân thành số thập phân
    so_thap_phan = int(nhi_phan, 2)
    # 2. Trừ đi khóa và chuyển lại thành chữ
    chu_cai = chr(so_thap_phan - khoa_giai_ma)
    tin_goc += chu_cai

print(f"Tin nhắn sau khi giải mã: {tin_goc}")
