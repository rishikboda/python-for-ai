
import turtle
import random
import math
screen=turtle.Screen()
screen.bgcolor("black")
t=turtle.Turtle()
t.speed(0)
t.hideturtle()
colors =[ "red","blue","yellow","orange","lime","white","pink","green"]
t.penup()
for i in range(300):
    t.pendown()
    t.color(random.choice(colors))
    t.forward(i*0.6)
    t.right(59)
    t.penup()
turtle.done()    
