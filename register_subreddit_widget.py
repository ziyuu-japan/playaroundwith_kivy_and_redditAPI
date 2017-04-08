from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from kivy.lang import Builder
Builder.load_string("""
<RegisterSubredditWidget>:
    orientation: 'vertical'
    SearchSubredditWidget:
        id: search_subreddit
    ShowResultsAndRegisterSubredditWidget:
        id: show_results_and_register_subreddit

<ShowResultsAndRegisterSubredditWidget>:
    Label:
        id: label
        text: ''
    Button:
        id: button
        text: 'Register'
        on_press: root.register_subreddit(args)

<SearchSubredditWidget>:
    Label:
        text: 'Search a subreddit you want to register'
    TextInput:
        id: search_subreddit_textinput
    Button:
        text: "Search"
        on_press: root.search_subreddit(args)
""")

class SearchSubredditWidget(BoxLayout):

    def search_subreddit(self, instance):
        # print(self.ids['search_subreddit_textinput'].text)
        text = self.ids['search_subreddit_textinput'].text
        self.parent.fire_show_results(text)


class ShowResultsAndRegisterSubredditWidget(BoxLayout):
    def show_results(self, text):
        print(text)
        import praw
        import prawcore
        info = App.get_running_app().info

        if info == {}:
            return

        reddit = praw.Reddit(client_id=info['client_id'], client_secret=info['client_secret'], password=info['password'],
                                    user_agent=info['user_agent'], username=info['username'])

        # reddit = praw.Reddit(client_id='RSb9Q8JEutDARg',
        #                      client_secret='eayRYP89RQc3k4BolV45Z9fzBcc',
        #                      password='forziyuu1111',
        #                      user_agent='test1 by /u/ziyuuu',
        #                      username='ziyuuu')
        try:
            subreddit = reddit.subreddit(text)
            print(subreddit.fullname)
        except praw.exceptions.PRAWException:
            print('praw.exceptions.PRAWException was detected.')
        except praw.exceptions.ClientException:
            print('praw.exceptions.ClientException was detected')
        except praw.exceptions.APIException:
            print('praw.exceptions.APIException')
        except prawcore.exceptions.NotFound:
            print('prawcore.NotFound')
        except prawcore.exceptions.Redirect:
            print('prawcore.exceptions.Redirect')
        except prawcore.exceptions.BadRequest:
            print('prawcore.exceptions.Redirect')
        except TypeError:
            print("Enter subreddit's name.")
        except Exception as e:
            print('Exception', e.value)
        else:
            self.ids['label'].text = text
            if text in App.get_running_app().registered_subreddits:
                self.ids['button'].text = 'Unregister'
            else:
                self.ids['button'].text = 'Register'


        #TODO: search subreddit and show label and register button

    def register_subreddit(self, instance):
        if self.ids['button'].text == 'Unregister':
            App.get_running_app().unregister_subreddit(self.ids['label'].text)
            self.ids['button'].text = 'Register'
            return
        # App.root.register_subreddit(self.ids['label'].text)
        print(type(App.get_running_app()))
        App.get_running_app().register_subreddit(self.ids['label'].text)
        print(App.get_running_app().registered_subreddits)
        self.ids['button'].text = 'Unregister'

class RegisterSubredditWidget(BoxLayout):
    def fire_show_results(self, text):
        self.ids['show_results_and_register_subreddit'].show_results(text)
