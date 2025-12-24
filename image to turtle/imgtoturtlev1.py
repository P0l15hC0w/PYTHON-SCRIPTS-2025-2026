from PIL import Image
import turtle
import math

img = Image.open("img.png").convert("RGB")

width, height = img.size

img = img.resize((math.ceil(width/2), math.ceil(height/2)))

width, height = img.size
pixels = img.load()

screen = turtle.Screen()
screen.setup(width*4, height*4)
turtle.colormode(255)

t = turtle.Turtle()

t.hideturtle()
t.penup()
t.speed(0)

turtle.tracer(0)

dot_size = 7

for y in range(height):

    for x in range(width):
        r, g, b = pixels[x, y]
        t.goto((x - width//2)*math.ceil(dot_size/2), (height//2 - y)*math.ceil(dot_size/2))
        t.pencolor(r, g, b)
        t.dot(dot_size)

    
turtle.update()
turtle.done()


