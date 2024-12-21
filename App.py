import tkinter as tk
import random
import math
import time

games = ["Test1", "Test2", "Test3"]

# Создаем словарь фиксированных цветов для каждой игры
game_colors = {
    "Test1": "#FF6B6B",  # Красный
    "Test2": "#4ECDC4",  # Бирюзовый
    "Test3": "#45B7D1",  # Голубой
}

def spin_wheel():
    selected_games = [game for game, var in check_vars.items() if var.get() == 1]
    if len(selected_games) < 2:
        result_label.config(text="Пожалуйста, выберите не менее 2 игр, чтобы запустить игру.")
        return

    wheel_canvas.delete("all")
    segment_angle = 360 / len(selected_games)
    
    # Начальный угол вращения
    current_angle = 0
    # Общее количество оборотов (уменьшено для более медленного старта)
    total_rotations = random.uniform(3, 5)
    # Увеличено количество кадров для более плавной анимации
    total_frames = 180
    
    def draw_wheel(angle):
        wheel_canvas.delete("all")
        for i, game in enumerate(selected_games):
            arc_start = segment_angle * i + angle
            # Используем фиксированный цвет для каждой игры
            color = game_colors[game]
            
            # Рисуем сегмент колеса
            wheel_canvas.create_arc(
                50, 50, 250, 250,
                start=arc_start,
                extent=segment_angle,
                fill=color
            )
            
            # Добавляем текст
            text_angle = math.radians(arc_start + segment_angle / 2)
            x = 150 + 80 * math.cos(text_angle)
            y = 150 - 80 * math.sin(text_angle)
            wheel_canvas.create_text(
                x, y,
                text=game,
                font=("Arial", 10),
                angle=90 + math.degrees(text_angle),
                fill="white"  # Белый текст для лучшей читаемости
            )
        
        # Указатель
        wheel_canvas.create_polygon(
            150, 40,
            140, 20,
            160, 20,
            fill="red"
        )
    
    def animate(frame):
        nonlocal current_angle
        if frame <= total_frames:
            # Модифицированная функция замедления
            progress = frame / total_frames
            
            # Используем более сложную функцию замедления
            # Начинается быстрее и замедляется более постепенно
            ease_out = 1 - math.pow(1 - progress, 4)
            
            # Добавляем небольшое колебание в конце
            if progress > 0.8:
                wobble = math.sin(progress * 10) * (1 - progress) * 5
                ease_out += wobble
            
            current_angle = total_rotations * 360 * ease_out
            
            draw_wheel(current_angle)
            # Уменьшаем частоту обновления для более медленного вращения
            delay = int(16 + (frame / total_frames) * 20)  # Постепенно увеличиваем задержку
            root.after(delay, lambda: animate(frame + 1))
        else:
            # Определяем победителя
            final_angle = current_angle % 360
            winning_segment = int((360 - final_angle) / segment_angle % len(selected_games))
            chosen_game = selected_games[winning_segment]
            result_label.config(text=f"Выбрана игра: {chosen_game}")
    
    animate(0)

# GUI Setup
root = tk.Tk()
root.title("Game Spinner")
root.geometry("600x600")

# Центрирование окна
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 600) // 2
y = (screen_height - 600) // 2
root.geometry(f"600x600+{x}+{y}")

instructions = tk.Label(root, text="Выберите не менее 2 игр, чтобы вращать колесо:")
instructions.pack(pady=10)

# Чекбоксы для выбора игр
check_vars = {}
for game in games:
    var = tk.IntVar()
    # Добавляем цветной индикатор рядом с чекбоксом
    frame = tk.Frame(root)
    frame.pack(anchor="w", padx=5)
    color_indicator = tk.Label(frame, text="■", fg=game_colors[game], font=("Arial", 16))
    color_indicator.pack(side="left", padx=5)
    check_button = tk.Checkbutton(frame, text=game, variable=var)
    check_button.pack(side="left")
    check_vars[game] = var

# Кнопка
spin_button = tk.Button(root, text="Spin the Wheel", command=spin_wheel)
spin_button.pack(pady=20)

# Холст для рисования колеса
wheel_canvas = tk.Canvas(root, width=300, height=300, bg="white")
wheel_canvas.pack()

# Результат
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()