from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from kivy.lang import Builder
Builder.load_string("""
<PrepareForRedditAPIWidget>:
    client_id: client_id_textinput
    client_secret: client_secret_textinput
    password: password_textinput
    user_agent: user_agent_textinput
    username: username_textinput
    save_button: save_button

    orientation: 'vertical'
    BoxLayout:
        Label:
            text: 'client_id'
        TextInput:
            id: client_id_textinput
    BoxLayout:
        Label:
            text: 'client_secret'
        TextInput:
            id: client_secret_textinput
    BoxLayout:
        Label:
            text: 'password'
        TextInput:
            id: password_textinput
    BoxLayout:
        Label:
            text: 'user_agent'
        TextInput:
            id: user_agent_textinput
    BoxLayout:
        Label:
            text: 'username'
        TextInput:
            id: username_textinput
    Button:
        id: save_button
        text: 'save'
        on_press: root.save(args)
""")

# import praw
# import prawcore
# reddit = praw.Reddit(client_id='RSb9Q8JEutDARg',
#                      client_secret='eayRYP89RQc3k4BolV45Z9fzBcc',
#                      password='forziyuu1111',
#                      user_agent='test1 by /u/ziyuuu',
#                      username='ziyuuu')

class PrepareForRedditAPIWidget(BoxLayout):
    client_id = ObjectProperty(None)
    client_secret = ObjectProperty(None)
    password = ObjectProperty(None)
    user_agent = ObjectProperty(None)
    username = ObjectProperty(None)
    save_button = ObjectProperty(None)


    def save(self, instance):
        if App.get_running_app().create_and_hold_reddit_instance(self.client_id.text, self.client_secret.text, self.password.text,
                                                                    self.user_agent.text, self.username.text):
            # It was succeeded to create a reddit instance
            self.save_button.text = 'save' + ':succeed'
        else:
            self.save_button.text = 'save' + ':fail please rewrite data'
