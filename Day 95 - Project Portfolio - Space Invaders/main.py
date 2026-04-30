from turtle import Screen
import time
import random
from functools import partial
from entities import Entity, Enemy, Player, Bullet, Score
from effects import Effects

ASSET_FOLDER = "./assets"
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)

INVADERS = ("green", "yellow", "red", "player")
INVADER_ASSETS = [f'/Invaders/{invader}.png' for invader in INVADERS]

EFFECTS = ("Exhaust_Fire_up", "Exhaust_Fire_down", "Explosion1", "Explosion2", "Explosion3", "Explosion4", "Explosion5")
EFFECT_ASSETS = [f'/Effects/{effect}.gif' for effect in EFFECTS]


SHIP = Enemy | Player

class SpaceInvaders:
    def __init__(self):
        self.player : Player | None = None
        self.enemies : list[Enemy] = []
        self.bullets: list[Bullet] = []

        self.running = True

        self.screen = Screen()
        self.effects = Effects(screen=self.screen)
        self.score_manager = Score()

        self.setup_game()

    def setup_game(self):
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.bgpic(f"{ASSET_FOLDER}/Effects/bg.png")
        self.screen.tracer(0)

        self.load_sprites()

        self.player = Player(start_pos=(0, -260))

        for _ in range(10):
            xcor = random.randrange(SCREEN_WIDTH // 2 * -1, SCREEN_WIDTH // 2)
            ycor = random.randrange(SCREEN_HEIGHT // 2 * -1, SCREEN_HEIGHT // 2)

            Entity(shape=None, start_pos=(xcor, ycor))

        self.screen.onkeypress(fun=self.player.move_right, key="Right")
        self.screen.onkeypress(fun=self.player.move_left, key="Left")
        self.screen.onkey(fun=lambda: (partial(self.shoot, entity=self.player)(),self.start_player_shoot_cooldown()), key="space")
        self.screen.listen()

    def load_sprites(self):
        for sprite in (INVADER_ASSETS + EFFECT_ASSETS):
            self.screen.register_shape(ASSET_FOLDER + sprite)

    def shoot(self, *, entity: SHIP):
        facing_directions = {
            Player : "N",
            Enemy : "S",
        }

        bullet_direction = facing_directions.get(type(entity))

        if bullet_direction is None:
            raise TypeError('Parameter "entity" must be of type Player or Enemy')

        if bullet_direction == "N":
            if not self.player.can_shoot:
                return

            else:
                self.player.can_shoot = False

        bullet = Bullet(facing=bullet_direction, from_pos=entity.pos())
        self.bullets.append(bullet)

    def move_bullets(self):
        for bullet in self.bullets[:]:
            bullet_ycor = bullet.ycor()

            if bullet_ycor > 250 or bullet_ycor < -300:
                self.bullets.remove(bullet)
                bullet.destroy()

            if bullet.facing == "N":
                if bullet_ycor < 60:
                    bullet.move()
                    continue

                for enemy in self.enemies[:]:
                    if bullet.collision(enemy):
                        bullet.destroy()
                        enemy.destroy()
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score_manager.increase_score()
                        break

                else:
                    bullet.move()

            else:
                if bullet_ycor > -200:
                    pass
                elif bullet.collision(self.player):
                    bullet.destroy()
                    self.bullets.remove(bullet)
                    self.running = False

                bullet.move()

    @property
    def can_spawn_enemies(self):
        return True if not self.enemies else False

    def spawn_enemies(self):
        screen_pos_width = int(SCREEN_WIDTH / 2)
        screen_neg_width = screen_pos_width * -1

        row_height = 300

        for _ in range(2):
            row_height -= 100
            for i in range(screen_pos_width-50, screen_neg_width, -50):
                e = Enemy(start_pos=(i, row_height))
                self.enemies.append(e)

    def start_player_shoot_cooldown(self):
        self.player.can_shoot = False
        self.screen.ontimer(t=1000, fun=partial(self.player.toggle_can_shoot, can_shoot=True))

    def run(self):
        self.effects.startup()

        while self.running:
            if self.can_spawn_enemies:
                if self.score_manager.score:
                    self.score_manager.increase_score(10)

                self.spawn_enemies()
                self.screen.update()
                time.sleep(0.8)
                continue

            self.move_bullets()

            for enemy in self.enemies:
                if random.randint(0, 100) == 0:
                    self.shoot(entity=enemy)

            self.screen.update()
            time.sleep(0.05)

        else:
            self.end_game()

    def restart_game(self):
        self.running = True
        self.score_manager.set_score(0)
        self.player.reset()

        for enemy in self.enemies:
            enemy.destroy()

        self.enemies.clear()
        self.bullets.clear()
        self.run()

    def end_game(self):
        self.effects.explosion(self.player.pos())
        self.player.destroy()

        for bullet in self.bullets:
            bullet.destroy()
            time.sleep(0.02)
            self.screen.update()

        self.restart_game()

def main() -> None:
    game = SpaceInvaders()
    game.run()


if __name__ == "__main__":
    main()

















