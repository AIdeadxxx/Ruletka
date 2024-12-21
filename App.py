import tkinter as tk
import random
import math
import time

games = ["Test1", "Test2", "Test3"]

# Основные цвета интерфейса
DARK_GRAY = "#1E1E1E"    # Темно-серый фон
LIGHT_GRAY = "#2D2D2D"   # Светло-серый для элементов
ACCENT_GRAY = "#3D3D3D"  # Акцентный серый
TEXT_COLOR = "#FFFFFF"    # Белый текст
HIGHLIGHT = "#4A4A4A"    # Подсветка для кнопок
WHEEL_TEXT_COLOR = "#000000"  # Черный текст для колеса

# Функция для генерации ярких цветов
def generate_bright_color():
    base_colors = [
        "#FF0000",  # Красный
        "#FF6B00",  # Оранжевый
        "#FFD700",  # Золотой
        "#00FF00",  # Зеленый
        "#00FFFF",  # Циан
        "#0080FF",  # Голубой
        "#8000FF",  # Фиолетовый
        "#FF00FF",  # Розовый
        "#FF0080",  # Малиновый
    ]
    return random.choice(base_colors)

# Генерируем случайные цвета при запуске
game_colors = {game: generate_bright_color() for game in games}

def spin_wheel():
    selected_games = [game for game, var in check_vars.items() if var.get() == 1]
    if len(selected_games) < 2:
        result_label.config(text="Пожалуйста, выберите не менее 2 игр, чтобы запустить игру.")
        return

    # Генерируем новые цвета при каждом запуске
    for game in selected_games:
        game_colors[game] = generate_bright_color()

    wheel_canvas.delete("all")
    segment_angle = 360 / len(selected_games)
    current_angle = 0
    total_rotations = random.uniform(3, 5)
    total_frames = 180
    
    def draw_wheel(angle):
        wheel_canvas.delete("all")
        
        # Рисуем внешний круг (обводка)
        wheel_canvas.create_oval(45, 45, 255, 255, outline=HIGHLIGHT, width=2)
        
        for i, game in enumerate(selected_games):
            arc_start = segment_angle * i + angle
            color = game_colors[game]
            
            # Рисуем сегмент
            wheel_canvas.create_arc(
                50, 50, 250, 250,
                start=arc_start,
                extent=segment_angle,
                fill=color,
                outline=HIGHLIGHT
            )
            
            # Добавляем текст черного цвета
            text_angle = math.radians(arc_start + segment_angle / 2)
            x = 150 + 80 * math.cos(text_angle)
            y = 150 - 80 * math.sin(text_angle)
            wheel_canvas.create_text(
                x, y,
                text=game,
                font=("Arial", 12, "bold"),  # Увеличил размер шрифта для лучшей читаемости
                angle=90 + math.degrees(text_angle),
                fill=WHEEL_TEXT_COLOR  # Черный текст
            )
        
        # Указатель
        wheel_canvas.create_polygon(
            150, 40,
            140, 20,
            160, 20,
            fill="#FF0000",
            outline=TEXT_COLOR,
            width=1
        )
    
    def animate(frame):
        nonlocal current_angle
        if frame <= total_frames:
            progress = frame / total_frames
            ease_out = 1 - math.pow(1 - progress, 4)
            
            if progress > 0.8:
                wobble = math.sin(progress * 10) * (1 - progress) * 5
                ease_out += wobble
            
            current_angle = total_rotations * 360 * ease_out
            draw_wheel(current_angle)
            delay = int(16 + (frame / total_frames) * 20)
            root.after(delay, lambda: animate(frame + 1))
        else:
            final_angle = current_angle % 360
            winning_segment = int((360 - final_angle) / segment_angle % len(selected_games))
            chosen_game = selected_games[winning_segment]
            result_label.config(text=f"Выбрана игра: {chosen_game}")
    
    animate(0)

# GUI Setup
root = tk.Tk()
root.title("Game Spinner")
root.geometry("600x600")

# Настройка темной темы
root.configure(bg=DARK_GRAY)

# Центрирование окна
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 600) // 2
y = (screen_height - 600) // 2
root.geometry(f"600x600+{x}+{y}")

# Стилизованные инструкции
instructions = tk.Label(
    root,
    text="Выберите не менее 2 игр, чтобы вращать колесо:",
    bg=DARK_GRAY,
    fg=TEXT_COLOR,
    font=("Arial", 10, "bold")
)
instructions.pack(pady=10)

# Рамка для чекбоксов
checkbox_frame = tk.Frame(root, bg=DARK_GRAY)
checkbox_frame.pack(pady=10)

# Чекбоксы для выбора игр
check_vars = {}
for game in games:
    var = tk.IntVar()
    frame = tk.Frame(checkbox_frame, bg=DARK_GRAY)
    frame.pack(anchor="w", padx=5, pady=2)
    
    # Цветной индикатор
    color_indicator = tk.Label(
        frame,
        text="■",
        fg=game_colors[game],
        bg=DARK_GRAY,
        font=("Arial", 16)
    )
    color_indicator.pack(side="left", padx=5)
    
    # Стилизованный чекбокс
    check_button = tk.Checkbutton(
        frame,
        text=game,
        variable=var,
        bg=DARK_GRAY,
        fg=TEXT_COLOR,
        selectcolor=LIGHT_GRAY,
        activebackground=DARK_GRAY,
        activeforeground=TEXT_COLOR
    )
    check_button.pack(side="left")
    check_vars[game] = var

# Стилизованная кнопка
spin_button = tk.Button(
    root,
    text="Spin the Wheel",
    command=spin_wheel,
    bg=LIGHT_GRAY,
    fg=TEXT_COLOR,
    activebackground=ACCENT_GRAY,
    activeforeground=TEXT_COLOR,
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=20,
    pady=10
)
spin_button.pack(pady=20)

# Холст для колеса
wheel_canvas = tk.Canvas(
    root,
    width=300,
    height=300,
    bg=DARK_GRAY,
    highlightthickness=0
)
wheel_canvas.pack()

# Стилизованная метка результата
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg=DARK_GRAY,
    fg=TEXT_COLOR
)
result_label.pack(pady=10)

root.mainloop()