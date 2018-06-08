import utilities as utils
import kivy
kivy.require('1.10.0')
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '850')



class MenuBar(Widget):
    pass

class DialogueView(Widget):
    pass

class ButtonBarA(AnchorLayout):

    pass

class ButtonBarAControls(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonBarAControls, self).__init__(**kwargs)
        self.labels = utils.load_labels(utils.ap_labels_path)

        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i], font_size='15',size_hint_max_x=160, size_hint_max_y=40)
            self.add_widget(btn)

class ButtonBarB(AnchorLayout):
    pass


class ButtonBarBControls(StackLayout):
    def __init__(self, **kwargs):
        super(ButtonBarBControls, self).__init__(**kwargs)

        labels = utils.load_labels(utils.da_labels_path)
        for i in range(len(labels)):
            btn = Button(text=labels[i], font_size='15', size_hint_max_x=160, size_hint_max_y=40)
            btn.bind(on_press=utils.callback)
            self.add_widget(btn)

class MainFrame(Widget):

    pass

class DialogueTaggerApp(App):

    def build(self):
        return MainFrame()

if __name__ == "__main__":
    DialogueTaggerApp().run()