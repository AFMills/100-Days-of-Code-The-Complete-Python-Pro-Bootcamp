from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()

def move_forwards():
    tim.forward(10)

def move_backwards():
    tim.backward(10)

def turn_left():
    tim.left(15)

def turn_right():
    tim.right(15)

def clear_screen():
    tim.clear()
    tim.teleport(0,0)
    tim.setheading(0)

screen.listen()
screen.onkey(move_forwards, "w")    # No parentheses after move_forwards, as we are inputting a function
screen.onkey(turn_left, "a")
screen.onkey(move_backwards, "s")
screen.onkey(turn_right, "d")
screen.onkey(clear_screen, "c")
screen.exitonclick()