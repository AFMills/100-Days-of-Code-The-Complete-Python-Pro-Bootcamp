from turtle import Turtle

MOVE_VALUE = 30

class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(position)
        self.start_position = position

    def go_right(self):
        new_x = self.xcor() + MOVE_VALUE
        if -310 < new_x < 310:
            self.hideturtle()
            self.goto(new_x, self.ycor())
            self.showturtle()

    def go_left(self):
        new_x = self.xcor() - MOVE_VALUE
        if -310 < new_x < 310:
            self.hideturtle()
            self.goto(new_x, self.ycor())
            self.showturtle()

    def reset_position(self):
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.goto(self.start_position)

    def shrink(self):
        self.shapesize(stretch_wid=1, stretch_len=4)