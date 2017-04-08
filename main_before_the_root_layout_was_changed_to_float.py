from kivy.config import Config

# Config.set('graphics', 'fullscreen', 'auto')
# Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'height', '50')

# Config.set('graphics', 'position', 'custom')
# Config.set('graphics', 'top', '0')
# Config.set('graphics', 'left', '0')
# kivy.metrics.dp(value)
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from preference_widget import PreferenceWidget
from main_display_widget import MainDisplayWidget

class RootWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.window_mode = 'normal' # not being preference mode
        self.main_display_widget = MainDisplayWidget()
        self.main_display_widget.size_hint_y = None
        self.main_display_widget.height = kivy.metrics.dp(50)
        self.preference_widget = PreferenceWidget()
        self.add_widget(self.main_display_widget)

    def switch_window_mode(self, instance):
        Window.size = (Window.size[0]/2, kivy.metrics.dp(500)/2)
        if self.window_mode == 'normal':
            self.window_mode = 'preference'
            Window.size = (Window.size[0]/2, kivy.metrics.dp(500)/2)
            self.clear_widgets()
            self.add_widget(self.main_display_widget)
        elif self.window_mode == 'preference':
            self.window_mode = 'normal'
            Window.size = (Window.size[0]/2, kivy.metrics.dp(50)/2)
        # self.clear_widgets()
        # print(self.ids)
        #print(self.ids['preference_widget'])


class MainApp(App):
    pass

if __name__ == '__main__':
    MainApp().run()
