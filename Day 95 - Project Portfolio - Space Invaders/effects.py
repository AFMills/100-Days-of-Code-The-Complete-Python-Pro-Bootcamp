from time import sleep
from entities import Entity, coordinate

ASSET_FOLDER = "./assets"
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)

EFFECTS = ("Exhaust_Fire_up", "Exhaust_Fire_down", "Explosion1", "Explosion2", "Explosion3", "Explosion4", "Explosion5")
EFFECT_ASSETS = [f'/Effects/{effect}.gif' for effect in EFFECTS]

class Effects:
    def __init__(self, screen):
        self.screen = screen

    def explosion(self, start_pos: coordinate, delay: float = 0.08, ticks: int=4):
        turtles = []
        main_t = Entity(start_pos=start_pos, visible=False)

        for i in range(1, ticks + 1):
            turt = main_t.clone()
            turt.shape(f"{ASSET_FOLDER}/Effects/Explosion{i}.gif")
            turtles.append(turt)

        for t in turtles:
            t.showturtle()
            self.screen.update()
            sleep(delay)
            t.destroy()

    def multi_explosion(self, coordinates: list[coordinate], delay: float = 0.08) -> None:
        turtles: list[list[Entity]] = []

        for coord in coordinates:
            turtles.append([Entity(visible=False, shape=f"{ASSET_FOLDER}/Effects/Explosion{sprite_num}.gif", start_pos=coord)
                            for sprite_num in range(1, 5)])

        turtle_queue: list[tuple[Entity]] = list(zip(*turtles))

        for tl in turtle_queue:
            for turt in tl:
                turt.showturtle()
            sleep(delay)
            self.screen.update()

        for idx, tl in enumerate(turtle_queue[::-1]):
            for turt in tl:
                turt.destroy()

    def startup(self):
        counter = Entity(start_pos=(-30, -20), visible=False)
        self.screen.update()

        for i in range(3, 0, -1):
            counter.write(i, font=("Courier", 100, "bold"))
            sleep(0.6)
            self.screen.update()
            counter.clear()

        coordinates = [xcor for xcor in range(SCREEN_WIDTH // 2 * -1, SCREEN_WIDTH // 2, 100)] + [400]
        sorted_coordinates = [0]

        for i in range(4, 0, -1):
            sorted_coordinates.extend([coordinates[i - 1], coordinates[i * -1]])

        self.multi_explosion([(xcor, 0) for xcor in sorted_coordinates])