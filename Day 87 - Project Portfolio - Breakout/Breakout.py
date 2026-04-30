import tkinter as tk
from turtle import Screen, Turtle
from paddle import Paddle
from brick import Brick
from ball import Ball
from scoreboard import Scoreboard
import time

SCREEN_WIDTH = 660
SCREEN_HEIGHT = 750
UPPER_BORDER = 300
LEFT_BORDER = -320
RIGHT_BORDER = 320
LEFT_BORDER_BRICKS = -280

POINTS = {
    "red" : 7,
    "orange" : 6,
    "yellow" : 5,
    "green":  4,
    "blue" : 3,
    "purple" : 2,
    "cyan" : 1
}

def collision(a, b):
    w = 0
    h = 0

    if b.turtlesize()[1] == 5:
        w = 60
    elif b.turtlesize()[1] == 4:
        w = 40

    if b.turtlesize()[0] == 1:
        h = 13
    elif b.turtlesize()[0] < 1:
        h = 7

    return (abs(a.xcor() - b.xcor()) < w) and (abs(a.ycor() - b.ycor()) < h)

class Breakout():
    def __init__(self):
        self.game_over = False
        self.game_is_on = True
        self.is_paused = False
        self.single_player = True

        self.paddle_is_small = False
        self.hit_yellow = False
        self.hit_red = None
        self.hit_upper_wall = False

        self.screen = Screen()
        self.screen.title("BREAKOUT")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)

        self.canvas = self.screen.getcanvas()
        self.timer_id = None

        self.pause = Turtle()
        self.start_splash = Turtle()
        self.g_o_screen = Turtle()
        self.count = Turtle()
        self.player_start_text = Turtle()

        self.paddle = Paddle((0, -330))
        self.ball = Ball()
        self.players = [Scoreboard(0), Scoreboard(1)]
        self.active_player = 0

        self.screen.onkey(self.paddle.go_left, "Left")
        self.screen.onkey(self.paddle.go_right, "Right")
        self.screen.onkey(self.toggle_gameplay, "space")
        self.screen.onkey(self.set_one_player, "a")
        self.screen.onkey(self.set_two_player, "b")
        self.screen.onkey(self.reload_game, 'y')
        self.screen.listen()

        self.bricks = []
        self.colors = ["red", "orange", "yellow", "green", "blue", "purple", "cyan"]

        self.brick_distance = 60
        self.x1 = LEFT_BORDER_BRICKS + 25
        self.y1 = UPPER_BORDER - self.brick_distance

        self.seconds_before_start = 3
        self.count_seconds = self.seconds_before_start

        self.brick_hits = 0
        self.frame = 0
        self.paddle_frame = 0
        self.brick_frame = 0

        self.splash_screen()

    def splash_screen(self):
        self.start_splash.hideturtle()
        self.start_splash.color("white")
        self.start_splash.penup()

        self.start_splash.goto(0, 50)
        self.start_splash.write("BREAKOUT", align="center", font=("Courier", 50, "normal"))

        self.start_splash.goto(0, 0)
        self.start_splash.write("Press 'a' to play singleplayer\n"
                                "Press 'b' to play with two players",
                                align="center",
                                font=("Courier", 15, "normal"))

        self.screen.exitonclick()

    def game_over_screen(self):
        self.g_o_screen.hideturtle()
        self.g_o_screen.color("white")
        self.g_o_screen.penup()
        self.g_o_screen.goto(0, 0)
        self.g_o_screen.write("GAME OVER", align="center", font=("Courier", 50, "normal"))
        self.g_o_screen.goto(0,-50)
        self.g_o_screen.write("Press 'y' for new game\n"
                              "Click to exit game",
                              align="center",
                              font=("Courier", 25, "normal"))
        self.screen.exitonclick()

    def toggle_gameplay(self):
        self.is_paused = not self.is_paused

        if not self.game_is_on:
            self.player_start_text.clear()
            self.game_is_on = True
            self.play_game()

    def reload_game(self):
        self.players[self.active_player].hits = 0
        self.paddle.reset_position()
        self.ball.reset_position(self.paddle.xcor(), -310)

        self.hit_yellow = False
        self.hit_red = False
        self.hit_upper_wall = False

        self.draw_bricks()
        self.draw_frame()

        if self.game_over:
            self.ball.reset_speed()
            self.g_o_screen.clear()
            for i in range(len(self.players)):
                self.players[i].reset_scoreboard()
            self.game_over = False

    def run_timer(self):
        if self.seconds_before_start >= 0:
            self.seconds_before_start -= 1

    def update(self):
        self.run_timer()
        self.count.clear()
        if self.seconds_before_start >= 0:
            self.count.write(f"{self.seconds_before_start}", align="center", font=("Courier", 50, "normal"))
            self.screen.ontimer(self.update, 1000)
        else:
            self.player_start_text.clear()
            self.game_is_on = True
            self.play_game()

    def ready_player(self):
        self.seconds_before_start = self.count_seconds
        self.count.clear()
        self.count.hideturtle()
        self.count.color("white")
        self.count.penup()
        self.count.goto(0, -150)

        if self.active_player == 0:
            p = "ONE"
        else:
            p = "TWO"

        self.player_start_text.hideturtle()
        self.player_start_text.color("white")
        self.player_start_text.penup()
        self.player_start_text.goto(0, -50)
        self.player_start_text.write(f"READY PLAYER {p}?", align="center", font=("Courier", 50, "normal"))

        self.update()

    def set_one_player(self):
        self.start_splash.clear()
        self.single_player = True
        self.reload_game()
        self.ready_player()

    def set_two_player(self):
        self.start_splash.clear()
        self.single_player = False
        self.reload_game()
        self.ready_player()

    def draw_bricks(self):
        for i in range(len(self.colors)):
            y_value = self.y1 - i * 25
            for j in range(7):
                x_value = self.x1 + j * (self.brick_distance + 25)
                b = Brick(x_value, y_value, self.colors[i])
                self.bricks.append(b)

    @staticmethod
    def draw_frame():
        frame = Turtle()

        frame.hideturtle()
        frame.color("grey")
        frame.penup()

        # LEFT SIDE OF FRAME
        frame.goto(LEFT_BORDER - 15, SCREEN_HEIGHT / 2)
        frame.setheading(180)
        frame.pendown()
        frame.begin_fill()

        for _ in range(2):
            frame.forward(30)
            frame.left(90)
            frame.forward(SCREEN_HEIGHT)
            frame.left(90)

        frame.end_fill()
        frame.penup()

        # MIDDLE OF FRAME
        frame.goto(-325, UPPER_BORDER)
        frame.setheading(0)
        frame.pendown()
        frame.begin_fill()

        for _ in range(2):
            frame.forward(SCREEN_WIDTH)
            frame.left(90)
            frame.forward(5)
            frame.left(90)

        frame.end_fill()
        frame.penup()

        #RIGHT SIDE OF FRAME
        frame.goto(RIGHT_BORDER + 15, SCREEN_HEIGHT / 2)
        frame.setheading(0)
        frame.pendown()
        frame.begin_fill()

        for _ in range(2):
            frame.forward(30)
            frame.right(90)
            frame.fd(SCREEN_HEIGHT)
            frame.right(90)

        frame.end_fill()
        frame.penup()

    def other_player(self):
        if self.active_player == 0:
            return 1
        else:
            return 0

    def play_game(self):
        if self.single_player:
            self.players[1].clear()
            self.players[1].game_over = True

        if self.timer_id is not None:
            self.canvas.after_cancel(self.timer_id)

        # MAIN LOOP
        while self.game_is_on:
            if self.is_paused:
                self.screen.update()
                self.pause.color("white")
                self.pause.hideturtle()
                self.pause.pu()
                self.pause.goto(0, -50)
                self.pause.write("PAUSE", align="center", font=("Courier", 100, "normal"))
            else:
                self.screen.update()
                self.frame += 1
                self.pause.clear()
                self.ball.move()

                if self.ball.xcor() > RIGHT_BORDER or self.ball.xcor() < LEFT_BORDER:
                    self.ball.bounce_x()

                if self.ball.ycor() > UPPER_BORDER:
                    self.ball.bounce_y()
                    if self.hit_upper_wall is False and self.hit_red is True:
                        self.hit_upper_wall = True
                        self.paddle.shrink()

                if collision(self.ball, self.paddle):
                    if (self.frame - self.paddle_frame) > 1:
                        self.ball.bounce_y()
                    self.paddle_frame = self.frame

                for br in self.bricks:
                    if collision(self.ball, br):
                        if (self.frame - self.brick_frame) > 1:
                            self.brick_frame = self.frame
                            br.delete()
                            self.bricks.remove(br)

                            self.players[self.active_player].hits += 1
                            self.ball.bounce_y()
                            self.players[self.active_player].add_point(POINTS[br.color()[0]])

                        if len(self.bricks) == 0:
                            self.players[self.active_player].level_up()
                            if not self.players[self.active_player].game_over:
                                self.game_is_on = False
                                self.reload_game()
                            else:
                                self.game_is_on = False
                                self.game_over_screen()

                        # Increase speed under specific conditions
                        if self.players[self.active_player].hits == 4 or self.players[self.active_player].hits == 12:
                            self.ball.increase_speed()
                        if "yellow" in br.color() and self.hit_yellow == False:
                            self.ball.increase_speed()

                        if "red" in br.color():
                            self.hit_red = True

                if self.ball.ycor() < -400:
                    self.players[self.active_player].lose_life()
                    self.ball.reset_position(self.paddle.xcor(), -300)

                    if self.players[self.active_player].game_over and self.players[self.other_player()].game_over:
                        self.game_is_on = False
                        self.game_over = True
                        self.game_over_screen()

                    elif self.players[self.active_player].game_over:
                        self.active_player = self.other_player()
                        self.game_is_on = False
                        self.reload_game()
                        self.ready_player()











