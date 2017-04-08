from kivy.config import Config

# Config.set('graphics', 'fullscreen', 'auto')
# Config.set('graphics', 'borderless', '1') # when not having a title bar, the up-left part is treated as (0, 0) of the window
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from preference_widget import PreferenceWidget
from main_display_widget import MainDisplayWidget
import praw
import prawcore



class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.window_mode = 'normal' # not being preference mode
        self.main_display_widget = MainDisplayWidget()
        self.main_display_widget.size_hint = (1, 1)
        self.main_display_widget.height = kivy.metrics.dp(50)
        self.preference_widget = PreferenceWidget()
        self.add_widget(self.main_display_widget)

    def switch_window_mode(self, instance):
        Window.size = (Window.size[0]/2, kivy.metrics.dp(500)/2)
        if self.window_mode == 'normal':
            self.window_mode = 'preference'
            Window.size = (Window.size[0]/2, kivy.metrics.dp(500)/2)
            self.clear_widgets()
            # self.main_display_widget.pos_hint = {'x': .1, 'y': .1}
            self.main_display_widget.pos = (kivy.metrics.dp(0), kivy.metrics.dp(450))
            self.main_display_widget.size_hint = (1, .1)
            self.add_widget(self.main_display_widget)
            self.preference_widget.pos = (kivy.metrics.dp(0), kivy.metrics.dp(0))
            self.preference_widget.size_hint = (1, .9)
            self.add_widget(self.preference_widget)
        elif self.window_mode == 'preference':
            self.window_mode = 'normal'
            Window.size = (Window.size[0]/2, kivy.metrics.dp(50)/2)
            self.clear_widgets()
            self.main_display_widget.size_hint = (1, 1)
            self.main_display_widget.pos = (kivy.metrics.dp(0), kivy.metrics.dp(0))
            self.add_widget(self.main_display_widget)


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.registered_subreddits = []
        self.info = {}

    def register_subreddit(self, text):
        print(text)
        self.registered_subreddits.append(text)
        print(self.registered_subreddits)

    def unregister_subreddit(self, text):
        print(text)
        self.registered_subreddits.remove(text)
        print(self.registered_subreddits)

    def create_and_hold_reddit_instance(self, client_id, client_secret, password,
                                        user_agent, username):
        try:
            reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             password=password,
                             user_agent=user_agent,
                             username=username)
            print(reddit.user.me())
        except prawcore.exceptions.RequestException:
            print('RequestException')
            return False # fail
        except prawcore.exceptions.OAuthException:
            print('OAuthException')
            return False
        except Exception as e:
            print('e.value')
            return False

        self.info = {}
        self.info['client_id'] = client_id
        self.info['client_secret'] = client_secret
        self.info['password'] = password
        self.info['user_agent'] = user_agent
        self.info['username'] = username

        return True # succeed

if __name__ == '__main__':
    MainApp().run()
