import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import math
import time
import os

# Структура данных для хранения информации об играх
class Game:
    def __init__(self, name, image_path=None):
        self.name = name
        self.image_path = image_path
        self.image = None
        self.thumbnail = None
        self.wheel_thumbnail = None
        if image_path and os.path.exists(image_path):
            self.load_image()

    def load_image(self):
        try:
            # Проверка существования файла
            if not os.path.exists(self.image_path):
                print(f"Файл не найден: {self.image_path}")
                return
        
            # Загружаем изображение для списка (50x50)
            img = Image.open(self.image_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            self.thumbnail = ImageTk.PhotoImage(img)
            
            # Загружаем изображение для колеса (40x40)
            wheel_img = Image.open(self.image_path)
            wheel_img = wheel_img.resize((80, 80), Image.Resampling.LANCZOS)
            self.wheel_thumbnail = ImageTk.PhotoImage(wheel_img)
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.thumbnail = None
            self.wheel_thumbnail = None

# Основные цвета интерфейса
DARK_GRAY = "#1E1E1E"
LIGHT_GRAY = "#2D2D2D"
ACCENT_GRAY = "#3D3D3D"
TEXT_COLOR = "#FFFFFF"
HIGHLIGHT = "#4A4A4A"
WHEEL_TEXT_COLOR = "#000000"

def generate_bright_color():
    base_colors = [
        "#FF0000", "#FF6B00", "#FFD700", "#00FF00",
        "#00FFFF", "#0080FF", "#8000FF", "#FF00FF", "#FF0080",
    ]
    return random.choice(base_colors)

# Словарь для хранения объектов игр
games = {
    "Stardew Valley": Game("Stardew Valley", image_path=r"Projeckt\Ruletka\Resurs\Снимок экрана 2024-12-21 032255.png"),
    "Starbound": Game("Starbound", image_path=r"Projeckt\Ruletka\Resurs\Снимок экрана 2024-12-21 032304.png"),
    "Terraria": Game("Terraria", image_path=r"Projeckt\Ruletka\Resurs\Снимок экрана 2024-12-21 032431.png")
}

# Принудительная загрузка картинок при создании
for game in games.values():
    game.load_image()


def update_game_list():
    # Обновляем отображение списка игр
    for widget in checkbox_frame.winfo_children():
        widget.destroy()
    
    for game_name, game in games.items():
        frame = tk.Frame(checkbox_frame, bg=DARK_GRAY)
        frame.pack(anchor="w", padx=5, pady=2)

        # Принудительная загрузка изображения
        game.load_image()
        
        # Изображение игры
        if game.thumbnail:
            img_label = tk.Label(frame, image=game.thumbnail, bg=DARK_GRAY)
            img_label.pack(side="left", padx=5)
        
        # Чекбокс
        var = tk.IntVar()
        check_button = tk.Checkbutton(
            frame,
            text=game_name,
            variable=var,
            bg=DARK_GRAY,
            fg=TEXT_COLOR,
            selectcolor=LIGHT_GRAY
        )
        check_button.pack(side="left")
        check_vars[game_name] = var

def spin_wheel():
    selected_games = [game for game, var in check_vars.items() if var.get() == 1]
    if len(selected_games) < 2:
        result_label.config(text="Пожалуйста, выберите не менее 2 игр, чтобы запустить игру.")
        return

    # Обновляем цвета
    for game in selected_games:
        game_colors[game] = generate_bright_color()

    wheel_canvas.delete("all")
    segment_angle = 360 / len(selected_games)
    current_angle = 0
    total_rotations = random.uniform(3, 5)
    total_frames = 180
    
    def draw_wheel(angle):
        wheel_canvas.delete("all")
        wheel_canvas.create_oval(45, 45, 255, 255, outline=HIGHLIGHT, width=2)
        
        for i, game_name in enumerate(selected_games):
            arc_start = segment_angle * i + angle
            color = game_colors[game_name]
            
            # Рисуем сегмент
            wheel_canvas.create_arc(
                50, 50, 250, 250,
                start=arc_start,
                extent=segment_angle,
                fill=color,
                outline=HIGHLIGHT
            )
            
            # Позиция для текста и изображения
            text_angle = math.radians(arc_start + segment_angle / 2)
            x = 150 + 80 * math.cos(text_angle)
            y = 150 - 80 * math.sin(text_angle)
            
            # Добавляем изображение, если оно есть
            game = games[game_name]
            
            # Добавляем текст
            wheel_canvas.create_text(
                x, y,
                text=game_name,
                font=("Arial", 12, "bold"),
                angle=90 + math.degrees(text_angle),
                fill=WHEEL_TEXT_COLOR
            )
        
        # Указатель
        wheel_canvas.create_polygon(
            150, 40, 140, 20, 160, 20,
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
root.geometry("600x700")  # Увеличил высоту для списка с картинками
root.configure(bg=DARK_GRAY)

# Центрирование окна
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 600) // 2
y = (screen_height - 700) // 2
root.geometry(f"600x700+{x}+{y}")

instructions = tk.Label(
    root,
    text="Выберите не менее 2 игр, чтобы вращать колесо:",
    bg=DARK_GRAY,
    fg=TEXT_COLOR,
    font=("Arial", 10, "bold")
)
instructions.pack(pady=10)

# Рамка для списка игр
checkbox_frame = tk.Frame(root, bg=DARK_GRAY)
checkbox_frame.pack(pady=10)

# Словарь для хранения переменных чекбоксов
check_vars = {}

# Словарь для хранения цветов
game_colors = {game: generate_bright_color() for game in games.keys()}

# Инициализация списка игр
update_game_list()

# Кнопка запуска
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

# Метка результата
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg=DARK_GRAY,
    fg=TEXT_COLOR
)
result_label.pack(pady=10)

root.mainloop()