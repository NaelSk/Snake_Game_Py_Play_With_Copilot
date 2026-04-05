import random
import threading
import time
import turtle
import winsound

# Window setup
wn = turtle.Screen()
wn.title("Sunny Snake")
wn.bgcolor("light goldenrod")
wn.setup(width=620, height=620)
wn.tracer(0)

# Playfield border
arena_pen = turtle.Turtle()
arena_pen.speed(0)
arena_pen.color("forest green")
arena_pen.pensize(4)
arena_pen.penup()
arena_pen.goto(-300, -300)
arena_pen.pendown()
for _ in range(4):
    arena_pen.forward(600)
    arena_pen.left(90)
arena_pen.hideturtle()

# Snake head
head = turtle.Turtle()
head.speed(0)
head.color("dark green", "lime green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

HEAD_STYLES = {
    "1": ("triangle", 1.1, 1.5),
    "2": ("classic", 1.0, 1.9),
    "3": ("square", 1.0, 1.5),
    "4": ("arrow", 1.0, 1.7),
    "5": ("circle", 1.0, 1.3),
}


def apply_head_style(style_key: str) -> None:
    shape_name, stretch_wid, stretch_len = HEAD_STYLES[style_key]
    head.shape(shape_name)
    head.shapesize(stretch_wid=stretch_wid, stretch_len=stretch_len)


def choose_head_style(style_key: str) -> None:
    global selecting_head
    if not selecting_head:
        return
    apply_head_style(style_key)
    selecting_head = False
    stop_intro_music()
    hide_head_options()


def select_head_1() -> None:
    choose_head_style("1")


def select_head_2() -> None:
    choose_head_style("2")


def select_head_3() -> None:
    choose_head_style("3")


def select_head_4() -> None:
    choose_head_style("4")


def select_head_5() -> None:
    choose_head_style("5")


apply_head_style("1")
head.setheading(90)

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("orange red")
food.penup()
food.goto(0, 100)

# Snake body segments
segments = []
obstacles = []

# Score
score = 0
high_score = 0
level = 1
max_level = 4
points_per_level = 100
delay = 0.1
game_over = False
game_won = False
selecting_head = True
intro_music_active = False
flash_state = False

pen = turtle.Turtle()
pen.speed(0)
pen.color("dark green")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write(
    f"Score: {score}  High: {high_score}  Level: {level}/{max_level}",
    align="center",
    font=("Courier", 16, "normal"),
)

message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color("dark green")
message_pen.penup()
message_pen.hideturtle()
message_pen.goto(0, 0)

shadow_pen = turtle.Turtle()
shadow_pen.speed(0)
shadow_pen.color("white")
shadow_pen.penup()
shadow_pen.hideturtle()
shadow_pen.goto(4, -4)

control_pen = turtle.Turtle()
control_pen.speed(0)
control_pen.color("dark olive green")
control_pen.penup()
control_pen.hideturtle()
control_pen.goto(0, -292)


def show_head_options() -> None:
    draw_start_screen()
    start_intro_music()
    control_pen.clear()
    control_pen.write(
        "Press 1-5: 1 Triangle  2 Classic  3 Square  4 Arrow  5 Circle",
        align="center",
        font=("Courier", 10, "normal"),
    )


def hide_head_options() -> None:
    message_pen.clear()
    shadow_pen.clear()
    control_pen.clear()


def draw_start_screen() -> None:
    shadow_pen.clear()
    message_pen.clear()
    shadow_pen.goto(4, -4)
    shadow_pen.write(
        "SELECT HEAD",
        align="center",
        font=("Courier", 38, "bold"),
    )
    message_pen.goto(0, 0)
    message_pen.write(
        "SELECT HEAD",
        align="center",
        font=("Courier", 38, "bold"),
    )
    message_pen.goto(0, -52)
    message_pen.write(
        "CHOOSE YOUR SNAKE STYLE",
        align="center",
        font=("Courier", 16, "normal"),
    )


def start_intro_music() -> None:
    global intro_music_active
    if intro_music_active:
        return
    intro_music_active = True

    # Original heroic arcade riff inspired by retro action games.
    melody = [
        (392, 120),
        (523, 120),
        (587, 120),
        (659, 180),
        (587, 120),
        (523, 120),
        (494, 180),
        (523, 120),
        (587, 120),
        (659, 180),
        (784, 240),
    ]

    def _play() -> None:
        while intro_music_active:
            for freq, duration in melody:
                if not intro_music_active:
                    return
                winsound.Beep(freq, duration)
                time.sleep(0.02)
            time.sleep(0.1)

    threading.Thread(target=_play, daemon=True).start()


def stop_intro_music() -> None:
    global intro_music_active
    intro_music_active = False


def play_eat_sound() -> None:
    """Ascending 8-bit style pickup blip (non-blocking)."""

    def _play():
        for freq in (600, 800, 1000):
            winsound.Beep(freq, 40)

    threading.Thread(target=_play, daemon=True).start()


def play_crash_sound() -> None:
    """Descending harsh crash tone (non-blocking)."""

    def _play():
        for freq in (400, 300, 200, 150):
            winsound.Beep(freq, 60)

    threading.Thread(target=_play, daemon=True).start()


def update_scoreboard() -> None:
    pen.clear()
    pen.write(
        f"Score: {score}  High: {high_score}  Level: {level}/{max_level}",
        align="center",
        font=("Courier", 16, "normal"),
    )


def draw_end_screen(title_text: str) -> None:
    shadow_pen.clear()
    message_pen.clear()
    shadow_pen.goto(4, -4)
    shadow_pen.write(
        title_text,
        align="center",
        font=("Courier", 38, "bold"),
    )
    message_pen.goto(0, 0)
    message_pen.write(
        title_text,
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
    pen.clear()  # Hide scoreboard during game-over display.
    draw_end_screen("GAME OVER")


def clear_game_over() -> None:
    message_pen.clear()
    shadow_pen.clear()


def trigger_game_over() -> None:
    global game_over
    game_over = True
    stop_intro_music()
    head.direction = "stop"
    show_game_over()


def trigger_win() -> None:
    global game_over, game_won
    game_over = True
    game_won = True
    stop_intro_music()
    head.direction = "stop"
    pen.clear()
    draw_end_screen("YOU WIN!")


def go_up() -> None:
    if selecting_head:
        return
    if head.direction != "down":
        head.direction = "up"
        head.setheading(90)


def go_down() -> None:
    if selecting_head:
        return
    if head.direction != "up":
        head.direction = "down"
        head.setheading(270)


def go_left() -> None:
    if selecting_head:
        return
    if head.direction != "right":
        head.direction = "left"
        head.setheading(180)


def go_right() -> None:
    if selecting_head:
        return
    if head.direction != "left":
        head.direction = "right"
        head.setheading(0)


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


def obstacle_positions() -> set[tuple[int, int]]:
    return {(int(obs.xcor()), int(obs.ycor())) for obs in obstacles}


def spawn_food() -> None:
    blocked = obstacle_positions()
    blocked.add((int(head.xcor()), int(head.ycor())))
    blocked.update({(int(seg.xcor()), int(seg.ycor())) for seg in segments})

    while True:
        fx = random.randint(-14, 14) * 20
        fy = random.randint(-14, 14) * 20
        if (fx, fy) not in blocked:
            food.goto(fx, fy)
            return


def spawn_one_obstacle() -> bool:
    blocked = obstacle_positions()
    blocked.add((int(head.xcor()), int(head.ycor())))
    blocked.add((int(food.xcor()), int(food.ycor())))
    blocked.update({(int(seg.xcor()), int(seg.ycor())) for seg in segments})

    # Keep the center area less crowded to make early gameplay fair.
    for _ in range(200):
        ox = random.randint(-14, 14) * 20
        oy = random.randint(-14, 14) * 20
        if abs(ox) <= 60 and abs(oy) <= 60:
            continue
        if (ox, oy) in blocked:
            continue

        obstacle = turtle.Turtle()
        obstacle.speed(0)
        obstacle.shape("square")
        obstacle.color("saddle brown")
        obstacle.penup()
        obstacle.goto(ox, oy)
        obstacles.append(obstacle)
        return True
    return False


def sync_level_obstacles() -> None:
    target_obstacles = level
    while len(obstacles) < target_obstacles:
        if not spawn_one_obstacle():
            break


def reset_game() -> None:
    global delay, score, level, game_won, selecting_head

    time.sleep(0.6)
    head.goto(0, 0)
    head.direction = "stop"
    head.setheading(90)

    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    for obs in obstacles:
        obs.goto(1000, 1000)
        obs.hideturtle()
    obstacles.clear()

    score = 0
    level = 1
    delay = 0.1
    game_won = False
    selecting_head = True
    sync_level_obstacles()
    spawn_food()
    show_head_options()
    update_scoreboard()


def replay() -> None:
    global game_over
    if game_over:
        clear_game_over()
        reset_game()
        game_over = False


sync_level_obstacles()
spawn_food()
show_head_options()


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
wn.onkeypress(select_head_1, "1")
wn.onkeypress(select_head_2, "2")
wn.onkeypress(select_head_3, "3")
wn.onkeypress(select_head_4, "4")
wn.onkeypress(select_head_5, "5")

# Main game loop
while True:
    wn.update()

    if not game_over:
        # Wall collision
        if abs(head.xcor()) > 300 or abs(head.ycor()) > 300:
            play_crash_sound()
            trigger_game_over()

        # Obstacle collision
        for obs in obstacles:
            if head.distance(obs) < 14:
                play_crash_sound()
                trigger_game_over()
                break

        # Food collision
        if not game_over and head.distance(food) < 20:
            spawn_food()

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("circle")
            new_segment.color("sea green")
            new_segment.penup()
            segments.append(new_segment)

            delay = max(0.04, delay - 0.002)
            score += 10
            level = min(max_level, score // points_per_level + 1)
            sync_level_obstacles()

            if score >= max_level * points_per_level:
                if score > high_score:
                    high_score = score
                update_scoreboard()
                trigger_win()
                continue

            if score > high_score:
                high_score = score
            update_scoreboard()
            play_eat_sound()

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
                play_crash_sound()
                trigger_game_over()
                break
    else:
        # Subtle blink effect for the game-over text.
        flash_state = not flash_state
        message_pen.color("dark green" if flash_state else "forest green")
        draw_end_screen("YOU WIN!" if game_won else "GAME OVER")

    time.sleep(delay)
