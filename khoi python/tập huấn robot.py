import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.datasets import load_diabetes

# --- PHẦN 1: KHỞI TẠO VÀ HUẤN LUYỆN MÔ HÌNH ---
print("--- 1. Khởi tạo và Huấn luyện Mô hình Random Forest ---")

# Tải dữ liệu và chuẩn bị
diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
y = pd.Series(diabetes.target)
cot_du_lieu = diabetes.feature_names # Tên 10 đặc trưng

# Tách dữ liệu thành tập huấn luyện (80%) và tập kiểm tra (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Định nghĩa mô hình Random Forest cơ bản và lưới siêu tham số
rf = RandomForestRegressor(random_state=42)
param_grid = {'n_estimators': [50, 100], 'max_depth': [None, 10]}

# Khởi tạo GridSearchCV: Dùng n_jobs=1 để khắc phục lỗi TerminatedWorkerError
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    scoring='r2',
    n_jobs=1, # Giảm tải cho CPU
    verbose=0
)

# Huấn luyện mô hình tốt nhất
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Đánh giá độ tin cậy R2 trên tập kiểm tra
r2_final = r2_score(y_test, best_model.predict(X_test))

print(f"Mô hình đã huấn luyện. R2 Score (Độ tin cậy): {r2_final:.2f}")

# --- PHẦN 2: HÀM NHẬP VÀ DỰ ĐOÁN TÙY CHỈNH ---

def nhap_du_lieu_tu_ban_phim():
    """Thu thập 10 giá trị đặc trưng từ người dùng qua bàn phím."""
    print("\n--- Nhập 10 Đặc trưng của Bệnh nhân Mới ---")
    print("LƯU Ý: Giá trị phải ở dạng số thập phân đã chuẩn hóa (ví dụ: 0.05, -0.01).")
    
    du_lieu_moi = []
    
    for ten_cot in cot_du_lieu:
        while True:
            try:
                # Nhập giá trị từ bàn phím
                gia_tri = float(input(f"Nhập giá trị cho {ten_cot} (Gợi ý: 0.00 là trung bình): "))
                du_lieu_moi.append(gia_tri)
                break
            except ValueError:
                print("⚠️ Lỗi: Vui lòng chỉ nhập số thập phân hợp lệ.")
    return du_lieu_moi

def du_doan_muc_do_benh(du_lieu_benh_nhan_moi):
    """
    Sử dụng mô hình đã huấn luyện để dự đoán mức độ tiến triển bệnh.
    (Đã bao gồm fix lỗi dự đoán cố định bằng NumPy)
    """
    
    # ⭐ BƯỚC KHẮC PHỤC: Chuyển list input thành NumPy array và reshape
    np_array = np.array(du_lieu_benh_nhan_moi).reshape(1, -1)
    
    # 1. Chuyển đổi NumPy array thành DataFrame
    data_df = pd.DataFrame(np_array, columns=cot_du_lieu)
    
    # 2. Thực hiện dự đoán
    du_doan = best_model.predict(data_df)
    
    # 3. Trả về kết quả dự đoán
    return du_doan[0]

# --- PHẦN 3: CHẠY CHƯƠNG TRÌNH ---

print("\n==============================================")
print("--- 'ROBOT TÍNH TOÁN' BỆNH TIỂU ĐƯỜNG ĐÃ SẴN SÀNG ---")
print("==============================================")

# Yêu cầu người dùng nhập dữ liệu
du_lieu_cua_ban = nhap_du_lieu_tu_ban_phim()

# Dự đoán bằng dữ liệu vừa nhập
ket_qua_du_doan = du_doan_muc_do_benh(du_lieu_cua_ban)

print("\n----------------------------------------------")
print(f"✅ Dữ liệu đầu vào của bạn (10 đặc trưng): {du_lieu_cua_ban}")
print(f"🎯 Mức độ Tiến triển Bệnh DỰ ĐOÁN: {ket_qua_du_doan:.2f}")
print("----------------------------------------------")
print(f"Thông tin độ tin cậy của Mô hình (R2 Score): {r2_final:.2f}")
print("==============================================")
