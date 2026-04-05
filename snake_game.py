import random
import time
import turtle

# Window setup
wn = turtle.Screen()
wn.title("Classic Snake")
wn.bgcolor("black")
wn.setup(width=620, height=620)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Snake body segments
segments = []

# Score
score = 0
high_score = 0
delay = 0.1
game_over = False
flash_state = False

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write(
    f"Score: {score}  High: {high_score}",
    align="center",
    font=("Courier", 16, "normal"),
)

message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color("cyan")
message_pen.penup()
message_pen.hideturtle()
message_pen.goto(0, 0)

shadow_pen = turtle.Turtle()
shadow_pen.speed(0)
shadow_pen.color("magenta")
shadow_pen.penup()
shadow_pen.hideturtle()
shadow_pen.goto(4, -4)


def update_scoreboard() -> None:
    pen.clear()
    pen.write(
        f"Score: {score}  High: {high_score}",
        align="center",
        font=("Courier", 16, "normal"),
    )


def draw_arcade_game_over() -> None:
    shadow_pen.clear()
    message_pen.clear()
    shadow_pen.goto(4, -4)
    shadow_pen.write(
        "GAME OVER",
        align="center",
        font=("Courier", 38, "bold"),
    )
    message_pen.goto(0, 0)
    message_pen.write(
        "GAME OVER",
        align="center",
        font=("Courier", 38, "bold"),
    )
    message_pen.goto(0, -52)
    message_pen.write(
        "PRESS R TO REPLAY",
        align="center",
        font=("Courier", 16, "normal"),
    )


def show_game_over() -> None:
    pen.clear()  # hide scoreboard
    draw_arcade_game_over()


def clear_game_over() -> None:
    message_pen.clear()
    shadow_pen.clear()


def trigger_game_over() -> None:
    global game_over
    game_over = True
    head.direction = "stop"
    show_game_over()


def go_up() -> None:
    if head.direction != "down":
        head.direction = "up"


def go_down() -> None:
    if head.direction != "up":
        head.direction = "down"


def go_left() -> None:
    if head.direction != "right":
        head.direction = "left"


def go_right() -> None:
    if head.direction != "left":
        head.direction = "right"


def move() -> None:
    x = head.xcor()
    y = head.ycor()

    if head.direction == "up":
        head.sety(y + 20)
    elif head.direction == "down":
        head.sety(y - 20)
    elif head.direction == "left":
        head.setx(x - 20)
    elif head.direction == "right":
        head.setx(x + 20)


def reset_game() -> None:
    global delay, score

    time.sleep(0.6)
    head.goto(0, 0)
    head.direction = "stop"

    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    score = 0
    delay = 0.1
    update_scoreboard()


def replay() -> None:
    global game_over
    if game_over:
        clear_game_over()
        reset_game()
        game_over = False


# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(replay, "r")
wn.onkeypress(replay, "R")

# Main game loop
while True:
    wn.update()

    if not game_over:
        # Wall collision
        if abs(head.xcor()) > 300 or abs(head.ycor()) > 300:
            trigger_game_over()

        # Food collision
        if head.distance(food) < 20:
            fx = random.randint(-14, 14) * 20
            fy = random.randint(-14, 14) * 20
            food.goto(fx, fy)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("green")
            new_segment.penup()
            segments.append(new_segment)

            delay = max(0.04, delay - 0.002)
            score += 10
            if score > high_score:
                high_score = score
            update_scoreboard()

        # Move body segments from tail to head
        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        if segments:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Self collision
        for seg in segments:
            if seg.distance(head) < 10:
                trigger_game_over()
                break
    else:
        # Subtle blink effect for an 80s arcade look.
        flash_state = not flash_state
        message_pen.color("cyan" if flash_state else "white")
        draw_arcade_game_over()

    time.sleep(delay)
