from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout


class MyApp(App):
    def build(self):
        # Основной макет
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Кнопка для вызова всплывающего окна
        popup_button = Button(text="Выберите игру", size_hint=(1, None) , height=50)
        popup_button.bind(on_press=self.show_popup)

        # Добавляем кнопку в макет
        layout.add_widget(popup_button)

        # Словарь для хранения состояний кнопок
        self.buttons_state = {
            "TestGame": False,
            "TestGame2": False,
            "TestGame3": False,
        }

        return layout

    def show_popup(self, instance):
        # Макет всплывающего окна
        popup_layout = GridLayout(cols=1, spacing=10, padding=10)

        # Создаем кнопки на основе текущего состояния
        self.buttons = {}
        for text, state in self.buttons_state.items():
            button = Button(
                text=text,
                size_hint_y=None,
                height=50,
                background_color=(0, 1, 0, 1) if state else (1, 1, 1, 1),
            )
            button.bind(on_press=self.toggle_button)
            popup_layout.add_widget(button)
            self.buttons[button] = text

        # Всплывающее окно
        popup = Popup(
            title="Пожалуйста, выберите не менее 2 игр, чтобы запустить колесо рулетку.",
            content=popup_layout,
            size_hint=(0.6, 0.6),
            auto_dismiss=True,
        )
        popup.open()

    def toggle_button(self, instance):
        # Меняем состояние кнопки
        button_text = self.buttons[instance]
        if self.buttons_state[button_text]:
            instance.background_color = (1, 1, 1, 1)  # Цвет по умолчанию (белый)
            self.buttons_state[button_text] = False
        else:
            instance.background_color = (0, 1, 0, 1)  # Зеленый цвет для выбранного
            self.buttons_state[button_text] = True

        print(f"Состояние кнопки '{button_text}': {'Выбрано' if self.buttons_state[button_text] else 'Не выбрано'}")


# Запуск приложения
if __name__ == '__main__':
    MyApp().run()
