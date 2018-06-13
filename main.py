
import kivy
from kivy.properties import ObjectProperty, StringProperty

from model import Dialogue

kivy.require('1.10.0')
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '850')

import controller
ctrl = controller.Controller()

class MainFrame(Widget):
    pass


class MenuBar(Widget):
    pass


# Dialogue View
class DialogueView(BoxLayout):


    pass


class NavButton(Button):
    def __init__(self, **kwargs):
        super(NavButton, self).__init__(**kwargs)

        self.bind(on_press=ctrl.next_prev)

    # def blah(self, instance):
    #     print("asdf")

class DialogueBox(BoxLayout):

    def __init__(self, **kwargs):
        super(DialogueBox, self).__init__(**kwargs)
        self.on_display_dialogue(ctrl.model.current_dialogue)

    def on_display_dialogue(self, instance):
        print("Here")
        for utt in instance.utterances:

            self.utterance_layout = BoxLayout(orientation='horizontal')
            utterance_btn = ToggleButton(text=utt.text, group='utt')
            utterance_ap_label = Label(text='AP Label', size_hint_x=0.1)
            utterance_da_label = Label(text='DA Label', size_hint_x=0.1)
            self.utterance_layout.add_widget(utterance_btn)
            self.utterance_layout.add_widget(utterance_ap_label)
            self.utterance_layout.add_widget(utterance_da_label)
            self.add_widget(self.utterance_layout)


# Button Bar A
class ButtonBarA(AnchorLayout):
    pass


class ButtonBarAControls(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonBarAControls, self).__init__(**kwargs)

        self.labels = ctrl.model.ap_labels

        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i], font_size='15',size_hint_max_x=160, size_hint_max_y=40)
            btn.bind(on_press=ctrl.add_label)
            self.add_widget(btn)


# Button Bar A
class ButtonBarB(AnchorLayout):
    pass


class ButtonBarBControls(StackLayout):
    def __init__(self, **kwargs):
        super(ButtonBarBControls, self).__init__(**kwargs)

        self.labels = ctrl.model.da_labels

        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i], font_size='15', size_hint_max_x=160, size_hint_max_y=40)
            btn.bind(on_press=ctrl.add_label)
            self.add_widget(btn)


class DialogueTaggerApp(App):
    def build(self):
        return MainFrame()


if __name__ == "__main__":
    DialogueTaggerApp().run()

