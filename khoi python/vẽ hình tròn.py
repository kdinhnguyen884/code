import turtle
r = int(input("Nhập lượng màu Đỏ (0-255): "))
g = int(input("Nhập lượng màu Xanh lá (0-255): "))
b = int(input("Nhập lượng màu Xanh dương (0-255): "))

# Chuyển từng số sang hệ 16, bỏ '0x', và đảm bảo có 2 chữ số (zfill)
hex_r = hex(r)[2:].zfill(2).upper()
hex_g = hex(g)[2:].zfill(2).upper()
hex_b = hex(b)[2:].zfill(2).upper()

ma_mau = "#" + hex_r + hex_g + hex_b
a = int(input("Nhập bán kính hình tròn: "))

screen = turtle.Screen()
t = turtle.Turtle()
screen.tracer(0)
t.hideturtle()

# Danh sách một vài mã màu hệ 16 đẹp

for i in range(2881):
    # Chọn màu dựa trên số dư của i (để xoay vòng các màu trong danh sách)
    t.color(ma_mau)
    
    t.forward(a)
    t.penup()
    t.backward(a)
    t.right(0.125)
    t.pendown()

screen.update()
print("Đã vẽ xong một bông hoa đa sắc!")
turtle.done()
