from turtle import Turtle

BASE_SPEED =1

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.x_move = 1
        self.y_move = 1
        self.move_speed = BASE_SPEED
        self.stopped = False
        self.speed(10)

    def move(self):
        if not self.stopped:
            new_x = self.xcor() + (self.x_move * self.move_speed)
            new_y = self.ycor() + (self.y_move * self.move_speed)

            self.hideturtle()
            self.goto(new_x, new_y)
            self.showturtle()

    def toggle_stop(self):
        if self.stopped:
            self.stopped = False
        else:
            self.stopped = True

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1

    def increase_speed(self):
        self.move_speed *= 1.1

    def reset_position(self, x, y):
        self.hideturtle()
        self.goto(x, y)
        self.showturtle()
        self.bounce_y()

    def reset_speed(self):
        self.move_speed = BASE_SPEED