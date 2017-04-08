import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.lang import Builder
Builder.load_string("""
<MainDisplayWidget>:
    size_hint_y: None
    BoxLayout:
        size_hint_x: .9
    Button:
        size_hint_x: .1
        text: 'test metrics'
        on_press: root.parent.switch_window_mode(args) # root.parent is referencing RootWidget instance
""")

class MainDisplayWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(MainDisplayWidget, self).__init__(**kwargs)
