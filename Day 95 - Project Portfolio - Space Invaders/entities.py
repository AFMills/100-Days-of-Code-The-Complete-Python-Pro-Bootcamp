from turtle import Turtle
import random

ASSET_FOLDER = "./assets"

INVADERS = ("green", "yellow", "red", "player")
INVADER_ASSETS = [f'/Invaders/{invader}.png' for invader in INVADERS]

EFFECTS = ("Exhaust_Fire_up", "Exhaust_Fire_down", "Explosion1", "Explosion2", "Explosion3", "Explosion4", "Explosion5")
EFFECT_ASSETS = [f'/Effects/{effect}.gif' for effect in EFFECTS]

coordinate = tuple[float, float]

class Entity(Turtle):
    def __init__(self, shape: str = None, start_pos: coordinate = (0, 0), visible: bool = True, facing_direction: float = 90):
        super(Entity, self).__init__(shape="classic" if shape is None else shape, visible=visible)
        self.penup()
        self.speed(0)
        self.setpos(start_pos)
        self.setheading(facing_direction)

    def destroy(self) -> None:
        self.reset()
        self.hideturtle()

class Enemy(Entity):
    def __init__(self, start_pos: coordinate = (0, 0)):
        super(Enemy, self).__init__(
            shape=ASSET_FOLDER + random.choice(INVADER_ASSETS[:-1]),
            start_pos=start_pos
        )

class Player(Entity):
    def __init__(self, start_pos: coordinate, visible=True):
        self._start_pos = start_pos
        self.can_shoot: bool = True

        super(Player, self).__init__(shape=ASSET_FOLDER + INVADER_ASSETS[-1], visible=visible, start_pos=start_pos)

    def move_right(self):
        if(curr_xcor := self.xcor()) < 370:
            self.setx(curr_xcor + 20)

    def move_left(self):
        if(curr_xcor := self.xcor()) > -370:
            self.setx(curr_xcor - 20)

    def toggle_can_shoot(self, can_shoot: bool) -> None:
        self.can_shoot = can_shoot

    def reset(self):
        self.setpos(self._start_pos)
        self.showturtle()

class Bullet(Entity):
    def __init__(self, *, facing: str, from_pos: coordinate):
        directions = {
            "N": {"sprite" : "Exhaust_Fire_up.gif", "facing_direction" : 90},
            "S": {"sprite" : "Exhaust_Fire_down.gif", "facing_direction" : 270}
        }

        val = directions.get(facing)
        if val is None:
            raise ValueError('"facing" must be either "N" or "S".')

        self.facing = facing

        super(Bullet, self).__init__(shape=f"{ASSET_FOLDER}/Effects/{val['sprite']}",
                                     start_pos=from_pos,
                                     facing_direction=val['facing_direction'])

        self.forward(20)

    @property
    def can_move(self) -> bool:
        xcor = self.xcor()
        ycor = self.ycor()
        return -480 < xcor < 480 and -320 < ycor < 320

    def move(self):
        self.forward(30)

    def collision(self, entity: Entity):
        return entity.distance(self.pos()) <= 40


class Score:
    def __init__(self):
        self.score = 0
        self.turt = Entity(start_pos=(320, -250), visible=False)
        self.update_score()

    def update_score(self):
        self.turt.clear()
        self.turt.write(self.score, font=("Courier", 40, "normal"))

    def increase_score(self, amount: int = 1):
        self.score += amount
        self.update_score()

    def set_score(self, amount):
        self.score = amount
        self.update_score()



















