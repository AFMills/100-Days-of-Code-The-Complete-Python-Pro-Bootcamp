import turtle as t
from turtle import Screen
import random

timmy = t.Turtle()
timmy.shape("turtle")
# timmy.color("red")

# # Draw a square
# for _ in range(4):
#     timmy.forward(100)
#     timmy.right(90)

# # Draw a dashed line
# for _ in range(5):
#     timmy.forward(10)
#     timmy.penup()
#     timmy.forward(10)
#     timmy.pendown()

# # Draw Shapes
# def draw_shape(num_sides):
#     for _ in range(num_sides):
#         angle = 360 / num_sides
#         timmy.right(angle)
#         timmy.forward(100)
#
# for sides in range(3, 11):
#     timmy.color(random.choice(colors))
#     draw_shape(sides)

# Random Walk with Random Colors
directions = [0, 90, 180, 270]
t.colormode(255)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color

# timmy.width(15)
# timmy.speed("fastest")
# for _ in range(200):
#     timmy.color(random_color())
#     timmy.setheading(random.choice(directions))
#     timmy.forward(30)

# Creates Spirograph
timmy.speed("fastest")

def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        timmy.color(random_color())
        timmy.circle(100)
        timmy.setheading(timmy.heading() + size_of_gap)

draw_spirograph(5)



# Must be the last declaration in the file
screen = Screen()
screen.exitonclick()