import turtle

wn = turtle.Screen()
wn.setup(width=600, height=400)
wn.tracer(0)

paddle = turtle.Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -150)

ball = turtle.Turtle()
ball.shape("circle")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2 # Tốc độ nhỏ lại một chút để bạn kịp phản ứng
ball.dy = 0.2

score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.penup()
pen.hideturtle()
pen.goto(0, 160)
pen.write("Điểm: 0", align="center", font=("Courier", 24, "normal"))

def sang_trai():
    x = paddle.xcor()
    if x > -250: # Giới hạn không cho thanh chạy ra ngoài màn hình
        paddle.setx(x - 20)

def sang_phai():
    x = paddle.xcor()
    if x < 250:
        paddle.setx(x + 20)

wn.listen()
wn.onkey(sang_trai, "Left")
wn.onkey(sang_phai, "Right")

try:
    while True:
        wn.update()
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Chạm tường trên
        if ball.ycor() > 190:
            ball.dy *= -1
        
        # Chạm tường trái/phải
        if ball.xcor() > 290 or ball.xcor() < -290:
            ball.dx *= -1

        # Chạm vào thanh hứng (Phần quan trọng nhất)
        if (ball.ycor() < -140 and ball.ycor() > -150) and (ball.xcor() < paddle.xcor() + 50 and ball.xcor() > paddle.xcor() - 50):
            ball.sety(-140)
            ball.dy *= -1
            score += 1
            pen.clear()
            pen.write(f"Điểm: {score}", align="center", font=("Courier", 24, "normal"))

        # Rơi ra ngoài (Thua)
        if ball.ycor() < -200:
            ball.goto(0, 0)
            ball.dy *= -1
    time.sleep(5)
except:
    print("Trò chơi kết thúc.")
