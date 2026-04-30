from turtle import Screen, Turtle
from snake import Snake
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)        # Turn off turtle animations

snake = Snake()

screen.listen()         # start listening for keystrokes
screen.onkey(snake.up, "Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")

game_is_on = True
while game_is_on:
    screen.update()       # Update the screen, since we turned off animations
    time.sleep(0.1)       # 0.1-second delay

    snake.move()



screen.exitonclick()