import turtle
import math

# Set up the turtle
turtle.shape("turtle")
turtle.fillcolor("green")
turtle.pensize(2)
turtle.speed(3)

# Position the turtle to center the pentagon better
turtle.penup()
turtle.goto(0, -80)
turtle.pendown()

# Point the turtle upward to start properly
turtle.setheading(90)

# Store pentagon vertices
vertices = []

# Start filling the shape
turtle.begin_fill()

# Draw a pentagon (5-sided shape) and store vertices
for i in range(5):
    vertices.append(turtle.position())  # Store current position
    turtle.forward(100)
    turtle.right(72)  # Turn RIGHT 72 degrees for exterior angle

# End filling the shape
turtle.end_fill()

# Change pen color for internal lines
turtle.pencolor("red")
turtle.pensize(1)

# Draw internal connections (pentagram star)
# Connect each vertex to the vertex 2 positions away
for i in range(5):
    turtle.penup()
    turtle.goto(vertices[i])
    turtle.pendown()
    # Connect to vertex that's 2 positions away (creates star pattern)
    turtle.goto(vertices[(i + 2) % 5])

# Keep the window open
turtle.done()