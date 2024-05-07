import tkinter
import random

ROWS = 20
COLS = 20
TILE_SIZE = 30

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def reset_game():
    global snake, food, velocityX, velocityY, snake_body, game_over, score
    # Initialize snake with a length of 3
    snake = [Tile(TILE_SIZE * 5, TILE_SIZE * 5), Tile(TILE_SIZE * 4, TILE_SIZE * 5), Tile(TILE_SIZE * 3, TILE_SIZE * 5)]
    snake_body = [Tile(TILE_SIZE * 5, TILE_SIZE * 5), Tile(TILE_SIZE * 4, TILE_SIZE * 5), Tile(TILE_SIZE * 3, TILE_SIZE * 5)]
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 1
    velocityY = 0
    game_over = False
    score = 0
    draw()


def move():
    global snake, food, snake_body, game_over, score

    # Move the snake
    new_head = Tile(snake[0].x + velocityX * TILE_SIZE, snake[0].y + velocityY * TILE_SIZE)

    # Check for collisions with walls
    if (new_head.x < 0 or new_head.x >= WINDOW_WIDTH or new_head.y < 0 or new_head.y >= WINDOW_HEIGHT):
        print("I DIED!")
        game_over = True
        return

    # Check for collision with snake's body
    for segment in snake_body[1:]:
        if new_head.x == segment.x and new_head.y == segment.y:
            print("I DIED!")
            game_over = True
            return

    # Update snake position
    snake.insert(0, new_head)
    snake_body.insert(0, Tile(new_head.x, new_head.y))  # Add new head to snake_body

    # Check for food collision
    if new_head.x == food.x and new_head.y == food.y:
        score += 1
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
    else:
        # Remove the last tail segment from snake_body
        snake_body.pop()


def draw():
    global snake, food, snake_body, game_over, score

    move()

    canvas.delete("all")

    # Draw grid lines
    for i in range(0, WINDOW_WIDTH, TILE_SIZE):
        canvas.create_line(i, 0, i, WINDOW_HEIGHT, fill="gray10")
    for j in range(0, WINDOW_HEIGHT, TILE_SIZE):
        canvas.create_line(0, j, WINDOW_WIDTH, j, fill="gray10")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red', outline="gray25")

    # Draw snake body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='dark green', outline="gray25")

    # Draw snake head
    canvas.create_rectangle(snake[0].x, snake[0].y, snake[0].x + TILE_SIZE, snake[0].y + TILE_SIZE, fill='lime green', outline="gray25")

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"Game Over: {score} \nClick Spacebar to Retry", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    if not game_over:
        window.after(100, draw)

def change_direction(e):
    global velocityX, velocityY, game_over
    if game_over:
        if e.keysym == "space":
            reset_game()
    else:
        if e.keysym == "Up" and velocityY != 1:
            velocityX = 0
            velocityY = -1
        elif e.keysym == "Down" and velocityY != -1:
            velocityX = 0
            velocityY = 1
        elif e.keysym == "Left" and velocityX != 1:
            velocityX = -1
            velocityY = 0
        elif e.keysym == "Right" and velocityX != -1:
            velocityX = 1
            velocityY = 0

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()

snake = [Tile(TILE_SIZE * 5, TILE_SIZE * 5), Tile(TILE_SIZE * 4, TILE_SIZE * 5), Tile(TILE_SIZE * 3, TILE_SIZE * 5)]
snake_body = [Tile(TILE_SIZE * 5, TILE_SIZE * 5), Tile(TILE_SIZE * 4, TILE_SIZE * 5), Tile(TILE_SIZE * 3, TILE_SIZE * 5)]
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 1
velocityY = 0
game_over = False
score = 0

draw()
window.bind("<KeyPress>", change_direction)
window.mainloop()
