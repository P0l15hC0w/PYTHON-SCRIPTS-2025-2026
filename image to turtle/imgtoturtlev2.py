from PIL import Image
import turtle
import math
import easygui

file_path = easygui.fileopenbox(title="Choose File",default="*.png", filetypes=["*.png", "*.jpeg", "*.jpg", "*.gif","*.tif", "*.tiff", "*.webp", "*.bmp"], multiple=False)

img = Image.open(file_path).convert("RGB") 
width, height = img.size

if height > 400:
    new_width = int(width * 400 / height)
    img = img.resize((new_width, 400))
    
if height < 1 or width < 1:
    img = img.resize((1, 1))

width, height = img.size
pixels = img.load()

screen = turtle.Screen()
screen.setup(math.ceil(width*1.2), math.ceil(height*1.2))
turtle.colormode(255)

t = turtle.Turtle()

t.hideturtle()
t.penup()
t.speed(0)

turtle.tracer(0)

pen_size = 1 
step = math.ceil(pen_size / 2)

for y in range(height):
    t.penup()
    t.goto((-width//2)*step, (height//2 - y)*step)
    t.pendown()
    
    for x in range(width):
        r, g, b = pixels[x, y]
        t.pencolor(r, g, b)
        t.forward(step)
    
    turtle.update()

turtle.done()
