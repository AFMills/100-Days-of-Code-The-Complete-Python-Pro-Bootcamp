from turtle import Turtle

FONT_SIZE = 40

class Scoreboard(Turtle):
    fontsize = FONT_SIZE
    def __init__(self, player):
        super().__init__()
        self.color("white")
        self.game_over = False
        self.penup()
        self.hideturtle()
        self.player = player
        self.score = 0
        self.highscore = 0
        self.lives = 3
        self.level = 1
        self.hits = 0

        self.update_scoreboard()

    def update_scoreboard(self):
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

        if self.player == 0:
            x1 = -290
            y1 = 340
            x2 = -280
            y2 = 310
            align = "left"

        else:
            x1 = 90
            y1 = 340
            x2 = 100
            y2 = 310
            align = "right"

        self.clear()

        self.goto(x1, y1)
        self.write(self.level, align = align, font=("Courier", FONT_SIZE - 20, "normal"))

        self.goto(x2, y2)
        self.write(f"{self.score:03d} ♥️ {self.lives}", align="left", font=("Courier", FONT_SIZE, "normal"))

    def reset_scoreboard(self):
        self.score = 0
        self.hits = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.update_scoreboard()

    def add_point(self, value):
        self.score += value
        self.update_scoreboard()

    def subtract_point(self):
        self.score -= 1
        self.update_scoreboard()

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        self.update_scoreboard()

    def level_up(self):
        self.level += 1
        if self.level > 2:
            self.game_over = True
            self.reset_scoreboard()
            if self.score > self.highscore:
                self.highscore = self.score


