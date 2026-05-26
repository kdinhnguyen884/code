import turtle
import random

# 1. Thiết lập màn hình
screen = turtle.Screen()
screen.setup(width=600, height=400)

# 2. Tạo rùa Đỏ
rua_do = turtle.Turtle()
rua_do.color("red")
rua_do.shape("turtle")
rua_do.penup()
rua_do.goto(-250, 50) # Vị trí xuất phát của rùa đỏ

# 3. Tạo rùa Xanh
rua_xanh = turtle.Turtle()
rua_xanh.color("blue")
rua_xanh.shape("turtle")
rua_xanh.penup()
rua_xanh.goto(-250, -50) # Vị trí xuất phát của rùa xanh

rua_ve = turtle.Turtle()
rua_ve.color("blue")
rua_ve.shape("turtle")
rua_ve.penup()
rua_ve.goto(230, 230)
rua_ve.pendown()
rua_ve.setheading(270)
rua_ve.forward(500)

# 4. Vòng lặp cuộc đua
dang_dua = True
while dang_dua:
    # Mỗi con tiến lên một khoảng ngẫu nhiên từ 1 đến 10
    rua_do.forward(random.randint(1, 10))
    rua_xanh.forward(random.randint(1, 10))

    # Kiểm tra xem có con nào chạm vạch đích (tọa độ x > 230) chưa
    if rua_do.xcor() > 230 or rua_xanh.xcor() > 230:
        dang_dua = False # Dừng cuộc đua
        
        if rua_do.xcor() > rua_xanh.xcor():
            print("Chúc mừng! Rùa ĐỎ đã thắng cuộc! 🎉")
        else:
            print("Chúc mừng! Rùa XANH đã thắng cuộc! 🎉")

turtle.done()
