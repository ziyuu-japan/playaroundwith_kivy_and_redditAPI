import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListView, ListItemButton, ListItemLabel
from kivy.core.audio import SoundLoader
from gtts import gTTS
from kivy.clock import Clock
import praw, prawcore

class ListingSubmissionsWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ListingSubmissionsWidget, self).__init__(**kwargs)
        # list_item_args_converter = \
        #         lambda row_index, rec: {'text': rec['title'],
        #                                 'size_hint_y': None,
        #                                 'height': 25}
        #
        # self.ambiguous_dictionary = self.get_data()
        #
        #
        # dict_adapter = DictAdapter(sorted_keys=sorted(self.ambiguous_dictionary.keys()),
        #                            data=self.ambiguous_dictionary,
        #                            args_converter=list_item_args_converter,
        #                            selection_mode='single',
        #                            allow_empty_selection=False,
        #                            cls=ListItemButton)
        #
        # master_list_view = ListView(adapter=dict_adapter)
        # self.add_widget(master_list_view)
        # self.label = Label(text='Init')
        # self.add_widget(self.label)
        # self.text_to_speech()

        # define this widget's initial state
        self.altanative_of_listview = Label(text='Empty')
        self.switch_button = Button(text='start')
        self.switch_button.bind(on_press=self.put_a_listview_and_start_to_speech)
        self.add_widget(self.switch_button)


    def put_a_listview_and_start_to_speech(self, instance):
        submissions_dictionary = self.load_submissions()
        if submissions_dictionary == {}:
            print('fail in load_submissions()')
            return

        listview_showing_submissions, dict_adapter = self.create_listview(submissions_dictionary)

        self.clear_widgets()
        self.add_widget(self.switch_button)
        self.add_widget(listview_showing_submissions)
        speech_index = 0
        self.start_to_speech(listview_showing_submissions, submissions_dictionary, dict_adapter, speech_index)

    def start_to_speech(self, listview, submissions_dictionary, dict_adapter, index, *args):
        if len(submissions_dictionary) == 0:
            return
        if [i for i in range(0, len(submissions_dictionary.keys()))][-1] < index:
            return
        print(args)
        # print(self.ambiguous_dictionary[sorted(self.ambiguous_dictionary.keys())[-1]])
        # value = self.ambiguous_dictionary.pop(sorted(self.ambiguous_dictionary.keys())[-1])
        # self.label.text = value['title']
        # self.clear_widgets()
        # self.add_widget(self.create_listview(self.ambiguous_dictionary))
        # self.add_widget(self.label)
        # print(value) ## TODO: Play a speech
        # retreave the speech time

        # print(dict_adapter.data)

        # dict_adapter.data =
        print(sorted(submissions_dictionary.keys()))
        tts = gTTS(text="{text}".format(text=str(index) + submissions_dictionary[str(index)]['title']), lang='en')
        tts.save("speeches/temp.mp3")
        sound = SoundLoader.load('speeches/temp.mp3')
        if sound:
            print("Sound found at %s" % sound.source)
            from mutagen.mp3 import MP3
            audio = MP3("speeches/temp.mp3")
            # print(audio.info.length)
            sound.play()
            from functools import partial
            Clock.schedule_once(partial(self.start_to_speech, listview, submissions_dictionary, dict_adapter, index+1), audio.info.length)

    def load_submissions(self):
        registered_subreddits = App.get_running_app().registered_subreddits
        if registered_subreddits == []:
            return {}

        info = App.get_running_app().info
        if info == {}:
            return {}

        reddit = praw.Reddit(client_id=info['client_id'],
                             client_secret=info['client_secret'],
                             password=info['password'],
                             user_agent=info['user_agent'],
                             username=info['username'])

        submissions_dictionary = {}
        submissions_dictionary_index = 0
        for registered_subreddit in registered_subreddits:
            submissions_dictionary[str(submissions_dictionary_index)] = {'title': registered_subreddit, 'url': ''}
            submissions_dictionary_index += 1
            for submission in reddit.subreddit(registered_subreddit).hot(limit=50):
                submissions_dictionary[str(submissions_dictionary_index)] = {'title': submission.title, 'url': submission.url}
                submissions_dictionary_index += 1

        return submissions_dictionary
        #self.create_listview(submissions_dictionary)

        # for index, submission in enumerate(subreddit.hot(limit=50)):
        #     #print(submission.title)
        #     ambiguous_dictionary[str(index)] = {'title': submission.title, 'url': submission.url}
        # return ambiguous_dictionary

    def create_listview(self, dict_data):
        list_item_args_converter = \
                lambda row_index, rec: {'text': str(row_index) + ' ' + rec['title'],
                                        'size_hint_y': None,
                                        'height': 25}

        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in range(0, len(dict_data.keys()))],
                                   data=dict_data,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=True,
                                   cls=ListItemLabel)

        master_list_view = ListView(adapter=dict_adapter)
        return master_list_view, dict_adapter


    def text_to_speech(self):
        self.show_text_and_play_a_speech()
        #self.label.text = self.ambiguous_dictionary.
        #Clock.schedule_once(my_popup.open, 5)

    def show_text_and_play_a_speech(self, *args):
        if len(self.ambiguous_dictionary) == 0:
            return
        print(self.ambiguous_dictionary[sorted(self.ambiguous_dictionary.keys())[-1]])
        value = self.ambiguous_dictionary.pop(sorted(self.ambiguous_dictionary.keys())[-1])
        self.label.text = value['title']
        self.clear_widgets()
        self.add_widget(self.create_listview(self.ambiguous_dictionary))
        self.add_widget(self.label)
        print(value) ## TODO: Play a speech
        # retreave the speech time
        tts = gTTS(text="{text}".format(text=value['title']), lang='en')
        tts.save("speeches/temp.mp3")
        sound = SoundLoader.load('speeches/temp.mp3')
        if sound:
            print("Sound found at %s" % sound.source)
            from mutagen.mp3 import MP3
            audio = MP3("speeches/temp.mp3")
            print(audio.info.length)
            sound.play()
            Clock.schedule_once(self.show_text_and_play_a_speech, audio.info.length)
        # after done, Clock

    def get_data(self):
        import praw

        info = App.get_running_app().info
        reddit = praw.Reddit(client_id=info['client_id'],
                             client_secret=info['client_secret'],
                             password=info['password'],
                             user_agent=info['user_agent'],
                             username=info['username'])

        subreddit = reddit.subreddit('redditdev')

        ambiguous_dictionary = {}
        for index, submission in enumerate(subreddit.hot(limit=50)):
            #print(submission.title)
            ambiguous_dictionary[str(index)] = {'title': submission.title, 'url': submission.url}
        return ambiguous_dictionary
