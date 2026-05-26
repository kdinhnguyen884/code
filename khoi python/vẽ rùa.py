import turtle
import random

# Tạo một chú rùa tên là 'my_turtle'
my_turtle = turtle.Turtle()

canh = int(input("nhập số cạch một hình"))
do_dai = int(input("nhập độ dài một cạnh"))
goc = 360 / canh
mau_sac = ["red", "blue", "green", "orange", "purple", "yellow"]


for i in range(canh + 1) :
    my_turtle.speed(0)
    my_turtle.color(random.choice(mau_sac))
    my_turtle.forward(do_dai)
    my_turtle.right(goc)
# Giữ cửa sổ vẽ không bị tắt ngay
turtle.done()
