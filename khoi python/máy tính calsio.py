x = int(input("Nhập số thứ nhất: "))
phep = input("Nhập phép tính (+, -, *, /): ")
q = int(input("Nhập số thứ hai: "))

if phep == "+":
    print(f"Kết quả: {x + q}")
elif phep == "-":
    print(f"Kết quả: {x - q}")
elif phep == "*":
    print(f"Kết quả: {x * q}")
elif phep == "/":
    if q == 0:
        print("Lỗi: Không thể chia cho số 0!")
    else:
        print(f"Kết quả: {x / q}")
else:
    print("Phép tính không hợp lệ!")
