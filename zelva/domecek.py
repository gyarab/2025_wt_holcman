from turtle import forward, left, exitonclick, right, up, degrees
from math import sqrt
from random import randint

def domecek(a):
    left(90)
    forward(a)
    right(90)
    forward(a)
    right(135)
    forward(sqrt(2*a**2))
    left(135)
    forward(a)
    left(135)
    forward(sqrt(2*a**2))
    right(90)
    forward((sqrt(2*a**2))/2)
    right(90)
    forward((sqrt(2*a**2))/2)
    right(45)
    forward(a)
    left(90)

def planeta(c):
    for i in range(c):
        domecek(randint(10, 20))
        right(360/c)

planeta(10)
exitonclick()