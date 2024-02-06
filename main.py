from tkinter import *
from tkinter import ttk
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 800
SPEED = 80
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Create Snake Body
        for _ in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        # Appending Snake Body
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="Snake")
            self.squares.append(square)

class Food:
    def __init__(self, snake):
        # Generate Food Placement
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]

        # Draw Food Object
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="Food")

def nextTurn(snake, food):
    global direction
    global direction_changed
    
    if not gameOverFlag:  # Only execute if game is not over
        x, y = snake.coordinates[0]

        if direction_changed:
            direction_changed = False

        if direction == "up":
            y -= SPACE_SIZE

        elif direction == "down":
            y += SPACE_SIZE

        elif direction == "left":
            x -= SPACE_SIZE

        elif direction == "right":
            x += SPACE_SIZE

        snake.coordinates.insert(0, (x, y))

        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.insert(0, square)

        # Food Eating
        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            label.config(text="Score:{}".format(score))
            canvas.delete("Food")
            food = Food(snake)

        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        # Collisions
        if checkCollisions(snake):
            gameOver()
        else:
            window.after(SPEED, nextTurn, snake, food)

def changeDirection(new_direction):
    global direction
    global direction_changed
    
    # Apply direction change only if it's not opposite to the current direction
    if (new_direction == 'left' and direction != 'right') or \
       (new_direction == 'right' and direction != 'left') or \
       (new_direction == 'up' and direction != 'down') or \
       (new_direction == 'down' and direction != 'up'):
        direction = new_direction
        direction_changed = True

def checkCollisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for bodyPart in snake.coordinates[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            return True

    return False

def gameOver():
    global gameOverFlag
    gameOverFlag = True
    
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50, font=('consolas', 70),
                       text="Game Over", fill="red", tag="GameOver")
    
    # Add Replay Button
    replay_button = ttk.Button(window, text="Replay", style='Replay.TButton', command=restartGame)
    replay_button_window = canvas.create_window(canvas.winfo_width() / 2 - 130, canvas.winfo_height() / 2 + 20, anchor='nw', window=replay_button)
    
    # Add Exit Button
    exit_button = ttk.Button(window, text="Exit", style='Exit.TButton', command=window.quit)
    exit_button_window = canvas.create_window(canvas.winfo_width() / 2 + 20 + 15, canvas.winfo_height() / 2 + 20, anchor='nw', window=exit_button)

def restartGame():
    global gameOverFlag
    global score
    global direction
    global direction_changed
    global snake
    global food
    
    gameOverFlag = False
    score = 0
    direction = 'down'
    direction_changed = False
    label.config(text="Score:{}".format(score))
    
    # Clear canvas
    canvas.delete("all")
    
    # Reset snake and food
    snake = Snake()
    food = Food(snake)
    
    # Start game again
    nextTurn(snake, food)

window = Tk()
window.title("Snake")
window.resizable(False, False)

# Custom styles for buttons
style = ttk.Style()
style.configure('Replay.TButton', foreground='green', font=('Helvetica', 14), padding=10)

style.configure('Exit.TButton', foreground='red', font=('Helvetica', 14), padding=10)

score = 0
direction = 'down'
direction_changed = False
gameOverFlag = False  # Flag to indicate if the game is over

# Score Label
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Canvas Creation
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


window.update()
windowWidth = window.winfo_width()
windowHeight = window.winfo_height()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

# Center Window
x = int((screenWidth / 2) - (windowWidth / 2))
y = int((screenHeight / 2) - (windowHeight / 2))
window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

# Key Binding
window.bind('<Left>', lambda event: changeDirection('left'))
window.bind('<Right>', lambda event: changeDirection('right'))
window.bind('<Up>', lambda event: changeDirection('up'))
window.bind('<Down>', lambda event: changeDirection('down'))

# Create Snake Object
snake = Snake()
food = Food(snake)

# Start game
nextTurn(snake, food)

window.mainloop()
