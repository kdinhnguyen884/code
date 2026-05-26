import random
import string

def tao_mat_khau(do_dai):
    # Tập hợp tất cả chữ cái, chữ số và ký hiệu
    ky_tu = string.ascii_letters + string.digits + string.punctuation
    
    # Chọn ngẫu nhiên các ký tự từ tập hợp trên
    mat_khau = ''.join(random.choice(ky_tu) for i in range(do_dai))
    
    return mat_khau

# Chạy thử
print("--- CÔNG CỤ TẠO MẬT KHẨU ---")
do_dai = int(input("Bạn muốn mật khẩu dài bao nhiêu ký tự? "))
print(f"Mật khẩu mới của bạn là: {tao_mat_khau(do_dai)}")
