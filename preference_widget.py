from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from move_entire_window_widget import MoveEntireWindowWidget
from register_subreddit_widget import RegisterSubredditWidget
from prepare_for_redditAPI_widget import PrepareForRedditAPIWidget
from listing_submissions_widget import ListingSubmissionsWidget


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<PreferenceWidget>:
    orientation: 'vertical'
    ListingSubmissionsWidget
    MoveEntireWindowWidget:
    RegisterSubredditWidget:
    PrepareForRedditAPIWidget:
""")

class PreferenceWidget(BoxLayout):
    pass
