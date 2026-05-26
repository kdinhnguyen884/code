import pandas as pd

data = {
    "Họ tên": ["Khôi", "Lan"],
    "Tuổi": [25, 22],
    "Lớp học": ["6D","7A"]
}

df = pd.DataFrame(data)
df.to_excel("du_lieu.xlsx", index=False)
print(df)
