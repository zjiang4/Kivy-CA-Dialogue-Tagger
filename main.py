import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.config import Config
# Configuration settings
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '800')

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy_utilities import ImageButton, ImageToggleButton, Separator
import controller

data_path = "data/"
dialogue_file = "test"
da_labels_file = "da_labels.txt"
ap_labels_file = "ap_labels.txt"

# Create controller
ctrl = controller.Controller(data_path, dialogue_file, da_labels_file, ap_labels_file)


# Root layout
class MainFrame(BoxLayout):
    def __init__(self, **kwargs):
        super(MainFrame, self).__init__(**kwargs)
        self.id = 'main_frame'

    def get_widget(self, widget_id):

        # Get root widgets children
        children = self.children[:]

        # Check each child
        while children:

            # Get the first child
            child = children.pop()
            # Add its children to the list
            children.extend(child.children)

            # Return if id's match
            if child.id == widget_id:
                return child


# Menu Bar
class MenuBar(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        self.id = 'menu_bar'

        self.padding = 5
        self.spacing = 5

        # Get initial state for labeled button
        if ctrl.get_mode():
            self.labeled_btn_state = 'normal'
        else:
            self.labeled_btn_state = 'down'

        # Buttons
        self.menu_btn = ImageButton(source='resources/menu_white.png', size=(40, 40), size_hint=(None, 1))
        self.menu_btn.bind(on_press=ctrl.menu)

        self.open_btn = ImageButton(source='resources/open_white.png', size=(40, 40), size_hint=(None, 1))
        self.open_btn.bind(on_press=ctrl.open_file)

        self.save_as_btn = ImageButton(source='resources/save_as_white.png', size=(40, 40), size_hint=(None, 1))
        self.save_as_btn.bind(on_press=ctrl.save_file_as)

        self.save_btn = ImageButton(source='resources/save_white.png', size=(40, 40), size_hint=(None, 1))
        self.save_btn.bind(on_press=ctrl.save_file)

        self.refresh_btn = ImageButton(source='resources/refresh_white.png', size=(40, 40), size_hint=(None, 1))
        self.refresh_btn.bind(on_press=ctrl.refresh)

        self.clear_btn = ImageButton(source='resources/clear_white.png', size=(40, 40), size_hint=(None, 1))
        self.clear_btn.bind(on_press=ctrl.clear)

        self.delete_btn = ImageButton(source='resources/delete_circle_red.png', size=(40, 40), size_hint=(None, 1))
        self.delete_btn.bind(on_press=ctrl.delete)

        self.labeled_btn = ImageToggleButton(source='resources/labelled_white.png', size=(40, 40), size_hint=(None, 1), group='mode')
        self.labeled_btn.bind(on_press=ctrl.toggle_mode)
        self.labeled_btn.state = self.labeled_btn_state

        self.add_widget(self.menu_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.open_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.save_as_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.save_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.refresh_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.clear_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.delete_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))
        self.add_widget(self.labeled_btn)
        self.add_widget(Separator(size_hint=(None, 1), width=1))

        # Create blank labels
        self.current_dialogue_id_lbl = Label(text='', size_hint=(None, 1))
        self.lbl_separator = Separator(size_hint=(None, 1), width=1)
        self.labeled_lbl = Label(text='', size_hint=(None, 1))
        self.unlabeled_lbl = Label(text='', size_hint=(None, 1))
        self.total_lbl = Label(text='', size_hint=(None, 1))

        # Display the stats labels
        self.display_stats(*ctrl.get_current_stats())

    def display_stats(self, dialogue_id='', labeled=0, unlabeled=0, total=0):

        # Clear old labels
        self.remove_widget(self.current_dialogue_id_lbl)
        self.remove_widget(self.lbl_separator)
        self.remove_widget(self.labeled_lbl)
        self.remove_widget(self.unlabeled_lbl)
        self.remove_widget(self.total_lbl)

        # Create the labels
        self.current_dialogue_id_lbl = Label(text='Current Dialogue: ' + dialogue_id, size_hint=(None, 1), width=200)
        self.lbl_separator = Separator(size_hint=(None, 1), width=1)
        self.labeled_lbl = Label(text='Labeled: ' + str(labeled), size_hint=(None, 1))
        self.unlabeled_lbl = Label(text='Unlabeled: ' + str(unlabeled), size_hint=(None, 1))
        self.total_lbl = Label(text='Total: ' + str(total), size_hint=(None, 1))

        # Add to the menu bar
        self.add_widget(self.current_dialogue_id_lbl)
        self.add_widget(self.lbl_separator)
        self.add_widget(self.labeled_lbl)
        self.add_widget(self.unlabeled_lbl)
        self.add_widget(self.total_lbl)


# Dialogue View
class DialogueView(BoxLayout):
    def __init__(self, **kwargs):
        super(DialogueView, self).__init__(**kwargs)
        self.id = 'dialogue_view'

    def next(self, instance):
        ctrl.next(instance)

    def prev(self, instance):
        ctrl.prev(instance)


# Dialogue Display Box
class DialogueBox(BoxLayout):
    def __init__(self, **kwargs):
        super(DialogueBox, self).__init__(**kwargs)
        self.id = 'dialogue_box'

        # Load initial dialogue to view
        self.display_dialogue(ctrl.get_current_dialogue())

    def display_dialogue(self, dialogue, selected_id=0):

        # Clear old layout
        self.clear_widgets()

        # Add each utterance to layout
        for i in range(len(dialogue.utterances)):

            # Create utterances layout
            utterance_layout = BoxLayout(orientation='horizontal')

            # Create utterances button
            utterance_btn = ToggleButton(text=dialogue.utterances[i].speaker + ":" + dialogue.utterances[i].text, id=str(i), group='utterances', allow_no_selection=False)
            utterance_btn.bind(on_press=ctrl.set_selected_utt)
            # Set default or currently selected button
            if i == selected_id:
                utterance_btn.state = 'down'

            # Create utterances labels
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
        self.labels = ctrl.get_ap_labels()

        # Create button layout
        self.btn_layout = StackLayout(size_hint=(0.9, 0.9), padding=5, spacing=5)
        self.add_widget(self.btn_layout)

        # Add buttons to layout
        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i],  id='btn_bar_a' + str(i), font_size='15', size_hint_max=(160, 40))
            btn.bind(on_press=ctrl.add_label)
            self.btn_layout.add_widget(btn)


# Button Bar B
class ButtonBarB(AnchorLayout):
    def __init__(self, **kwargs):
        super(ButtonBarB, self).__init__(**kwargs)
        self.id = 'button_bar_b'

        # Get button labels
        self.labels = ctrl.get_da_labels()

        # Create button layout
        self.btn_layout = StackLayout(size_hint=(0.9, 0.9), padding=5, spacing=5)
        self.add_widget(self.btn_layout)

        # Add buttons to layout
        for i in range(len(self.labels)):
            btn = Button(text=self.labels[i], id='btn_bar_b' + str(i), font_size='15', size_hint_max=(160, 40))
            btn.bind(on_press=ctrl.add_label)
            self.btn_layout.add_widget(btn)


class DialogueTaggerApp(App):
    icon = 'resources/nd-logo.ico'
    title = 'Dialogue Tagger'

    def build(self):
        return MainFrame()


if __name__ == "__main__":
    DialogueTaggerApp().run()

