\import random

def tro_choi_doan_so():
    # Máy tính chọn ngẫu nhiên 1 số từ 1 đến 100
    so_may_chon = random.randint(1, 100)
    
    print("Chào mừng bạn đến với trò chơi đoán số!")
    print("Mình đã chọn một số trong khoảng từ 1 đến 100. Đố bạn biết là số nào?")

    while True:
        try:
            # Lấy dữ liệu nhập từ người dùng
            du_doan = int(input("Nhập số bạn đoán: "))

            if du_doan > so_may_chon:
                print("Nhỏ hơn chút! 👇")
            elif du_doan < so_may_chon:
                print("Lớn hơn nữa! 👆")
            else:
                print(f"Chúc mừng! Bạn đã đoán đúng số {so_may_chon} rồi! 🎉")
                break # Thoát vòng lặp khi đoán đúng
        except ValueError:
            print("Vui lòng chỉ nhập số thôi nhé!")

# Chạy trò chơi
if __name__ == "__main__":
    tro_choi_doan_so()
