from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from screens.about_screen import AboutScreen
from screens.db_control import StudentManagementScreen
from screens.contact_screen import ContactScreen

from sqlalchemy import create_engine

class NavigationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_screen = 1

        # Database engine setup
        engine = create_engine('sqlite:///students.db')

        main_layout = FloatLayout()
        background = Image(source='space.png', fit_mode="fill")
        main_layout.add_widget(background)

        self.screen_manager = ScreenManager(transition=SlideTransition(duration=0.2))
        self.screen_manager.size_hint = (1, 0.9)
        self.screen_manager.pos_hint = {'top': 1}

        screen1 = Screen(name='screen1')
        screen1.add_widget(StudentManagementScreen(engine))

        screen2 = Screen(name='screen2')
        screen2.add_widget(ContactScreen(engine))

        screen3 = Screen(name='screen3')
        screen3.add_widget(AboutScreen(name="image"))

        self.screen_manager.add_widget(screen1)
        self.screen_manager.add_widget(screen2)
        self.screen_manager.add_widget(screen3)

        main_layout.add_widget(self.screen_manager)
        self.create_navigation_buttons(main_layout)
        self.add_widget(main_layout)


    def create_navigation_buttons(self, layout):
        # Создаем горизонтальный макет для кнопок
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'bottom': 1})

        # Создаем кнопки
        button1 = Button(text='DataBase')
        button2 = Button(text='Map')
        button3 = Button(text='About App')

        # Привязываем переключение экрана к кнопкам
        button1.bind(on_release=lambda x: self.switch_screen(1))
        button2.bind(on_release=lambda x: self.switch_screen(2))
        button3.bind(on_release=lambda x: self.switch_screen(3))

        # Добавляем кнопки в макет
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        # Добавляем макет с кнопками в основной layout
        layout.add_widget(button_layout)

    def switch_screen(self, target_screen):
        if target_screen != self.current_screen:
            if target_screen > self.current_screen:
                self.screen_manager.transition.direction = 'left'
            else:
                self.screen_manager.transition.direction = 'right'
            self.screen_manager.current = f'screen{target_screen}'
            self.current_screen = target_screen

class MyApp(App):
    def build(self):
        # Инициализация ScreenManager
        screen_manager = ScreenManager()

        screen_manager.add_widget(NavigationScreen())
        
        return screen_manager


if __name__ == "__main__":
    # Устанавливаем размеры окна для тестирования на ПК
    Window.size = (750/2, 1334/2)
    MyApp().run()
