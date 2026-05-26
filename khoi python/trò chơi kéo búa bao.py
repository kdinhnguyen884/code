import random

lua_chon = ["keo", "bua", "bao"]
may_chon = random.choice(lua_chon)

# Lấy lựa chọn của bạn
ban_chon = input("Nhập keo, bua hoặc bao: ").lower() # .lower() để nhập chữ HOA vẫn hiểu

print(f"Máy chọn: {may_chon}")

# So sánh kết quả
if ban_chon == may_chon:
    print("Hòa rồi! 🤝")
elif (ban_chon == "bua" and may_chon == "keo"):
    print("Bạn thắng! Búa đập được Kéo. 🔨")
elif (ban_chon == "keo" and may_chon == "bao"):
    print("Bạn thắng! Kéo cắt được Bao. ✂️")
elif (ban_chon == "bao" and may_chon == "bua"):
    print("Bạn thắng! Bao vây được Búa. 📄")
else:
    # Tất cả các trường hợp còn lại là bạn thua
    print("Bạn thua rồi! Chúc may mắn lần sau. 😢")
