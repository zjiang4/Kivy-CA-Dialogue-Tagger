from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

import controller
import kivy
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

# Create controller
ctrl = controller.Controller()


class MainFrame(BoxLayout):
    def __init__(self, **kwargs):
        super(MainFrame, self).__init__(**kwargs)
        self.id = 'main_frame'

    def get_widget(self, id):
        children = self.children[:]
        while children:
            child = children.pop()
            if child.id == id:
                return child
            children.extend(child.children)


class MenuBar(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        self.id = 'menu_bar'

        self.padding = 5
        self.spacing = 5

        self.menu_btn_layout = AnchorLayout(anchor_x='center', anchor_y='center', width=50, size_hint=(None, 1))
        self.menu_btn = Button(size=(40, 40))
        self.menu_btn.bind(on_press=ctrl.menu)
        self.menu_img = Image(source='resources/menu.png', height=40, width=40)
        self.menu_btn_layout.add_widget(self.menu_btn)
        self.menu_btn_layout.add_widget(self.menu_img)

        self.save_btn_layout = AnchorLayout(anchor_x='center', anchor_y='center', width=50, size_hint=(None, 1))
        self.save_btn = Button(size=(40, 40))
        self.save_btn.bind(on_press=ctrl.save)
        self.save_img = Image(source='resources/save.png', height=40, width=40)
        self.save_btn_layout.add_widget(self.save_btn)
        self.save_btn_layout.add_widget(self.save_img)

        self.refresh_btn_layout = AnchorLayout(anchor_x='center', anchor_y='center', width=50, size_hint=(None, 1))
        self.refresh_btn = Button(size=(40, 40))
        self.refresh_btn.bind(on_press=ctrl.refresh)
        self.refresh_img = Image(source='resources/refresh.png', height=40, width=40)
        self.refresh_btn_layout.add_widget(self.refresh_btn)
        self.refresh_btn_layout.add_widget(self.refresh_img)

        self.add_widget(self.menu_btn_layout)
        self.add_widget(self.save_btn_layout)
        self.add_widget(self.refresh_btn_layout)


# Dialogue View
class DialogueView(BoxLayout):
    def __init__(self, **kwargs):
        super(DialogueView, self).__init__(**kwargs)
        self.id = 'dialogue_view'

        with self.canvas:  # Instead of Kivy?
            Color(53 / 255.0, 53 / 255.0, 53 / 255.0, 1)
            self.rect = Rectangle(source='resources/background.png', pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):# Instead of Kivy?
        self.rect.pos = self.pos
        self.rect.size = self.size

    def next(self, instance):
        ctrl.next(instance)

    def prev(self, instance):
        ctrl.prev(instance)


class DialogueBox(BoxLayout):
    def __init__(self, **kwargs):
        super(DialogueBox, self).__init__(**kwargs)
        self.id = 'dialogue_box'

        # with self.canvas:# Instead of Kivy?
        #     # Color(0, 1, 0, 1)
        #     self.rect = Rectangle(source='resources/background.png', pos=self.pos, size=self.size)
        # self.bind(pos=self.update_rect, size=self.update_rect)

        # Load initial dialogue to view
        self.display_dialogue(ctrl.model.current_dialogue)

    def update_rect(self, *args):# Instead of Kivy?
        self.rect.pos = self.pos
        self.rect.size = self.size

    def display_dialogue(self, dialogue, selected_id=0):

        # Clear old layout
        self.clear_widgets()

        # Add each utterance to layout
        for i in range(len(dialogue.utterances)):

            # Utterances layout
            utterance_layout = BoxLayout(orientation='horizontal')

            # Utterances button
            utterance_btn = ToggleButton(text=dialogue.utterances[i].text, id=str(i), group='utterances')
            utterance_btn.bind(on_press=ctrl.set_selected_utt)
            # Set default or currently selected button
            if i == selected_id:
                utterance_btn.state = 'down'

            # Utterances labels
            utterance_ap_label = Label(text=dialogue.utterances[i].ap_label, size_hint_x=0.1)
            utterance_da_label = Label(text=dialogue.utterances[i].da_label, size_hint_x=0.1)

            # Add button and labels to layout
            utterance_layout.add_widget(utterance_btn)
            utterance_layout.add_widget(utterance_ap_label)
            utterance_layout.add_widget(utterance_da_label)

            self.add_widget(utterance_layout)


# Button Bar A
class ButtonBarA(AnchorLayout):
    def __init__(self, **kwargs):
        super(ButtonBarA, self).__init__(**kwargs)
        self.id = 'button_bar_a'

        # Get button labels
        self.labels = ctrl.model.ap_labels

        # Create button layout
        self.btn_layout = BoxLayout(size_hint=(None, 1), width=650, padding=5, spacing=5)
        self.add_widget(self.btn_layout)

        # Add buttons to layout
        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i], font_size='15', size_hint_max_x=160, size_hint_max_y=40)
            btn.bind(on_press=ctrl.add_ap_label)
            self.btn_layout.add_widget(btn)


# Button Bar B
class ButtonBarB(AnchorLayout):
    def __init__(self, **kwargs):
        super(ButtonBarB, self).__init__(**kwargs)
        self.id = 'button_bar_b'

        # Get button labels
        self.labels = ctrl.model.da_labels

        # Create button layout
        self.btn_layout = StackLayout(size_hint=(0.9, 0.9), padding=5, spacing=5)
        self.add_widget(self.btn_layout)

        # Add buttons to layout
        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i], font_size='15', size_hint_max_x=160, size_hint_max_y=40)
            btn.bind(on_press=ctrl.add_da_label)
            self.btn_layout.add_widget(btn)


class DialogueTaggerApp(App):
    icon = 'resources/nd-logo.ico'
    title = 'Dialogue Tagger'

    def build(self):
        return MainFrame()


if __name__ == "__main__":
    DialogueTaggerApp().run()

