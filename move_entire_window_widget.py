from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from kivy.lang import Builder
Builder.load_string("""
<MoveEntireWindowWidget>:
    window_x_pos: window_x_pos_textinput
    window_y_pos: window_y_pos_textinput

    Label:
        text: 'x'
    TextInput:
        id: window_x_pos_textinput
    Label:
        text: 'y'
    TextInput:
        id: window_y_pos_textinput
    Button:
        text: "Apply"
        on_press: root.apply_changed_position(args)
""")

class MoveEntireWindowWidget(BoxLayout):
    window_x_pos = ObjectProperty(None)
    window_y_pos = ObjectProperty(None)

    def apply_changed_position(self, instance):
        print("aaa")
        Window.top = int(self.window_y_pos.text)
        Window.left = int(self.window_x_pos.text)
