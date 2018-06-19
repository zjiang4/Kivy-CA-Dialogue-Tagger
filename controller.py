from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from model import Model


class Controller:

    def __init__(self):
        model = Model()
        self.model = model

    def menu(self, instance):
        print('The button <menu> is being pressed')

    def save(self, instance):
        print('The button <save> is being pressed')

    def refresh(self, instance):
        print('The button <refresh> is being pressed')

    def update_dialogue(self, selected_id=0):

        # Get dialogue box and call update function
        app = App.get_running_app()
        dialogue_box = app.root.get_widget('dialogue_box')
        dialogue_box.display_dialogue(self.model.current_dialogue, selected_id)

    def set_selected_utt(self, instance):

        # Get the selected button
        buttons = ToggleButton.get_widgets('utterances')

        for btn in buttons:
            if btn.state == 'down':
                # Set the corresponding utterance as selected in the model
                self.model.current_dialogue.set_current_utt(int(btn.id))
                print("Utterance index: " + btn.id + " Utt: " + btn.text)

    def prev(self, instance):
        print('The button <prev> is being pressed')
        ####SAVE!!!####

        # Set current dialogue utterance index to 0
        self.model.current_dialogue.set_current_utt(0)

        print("Index before: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)
        # Decrement dialogue
        self.model.dec_current_dialogue()
        print("Index after: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)

        # Update dialogue view
        self.update_dialogue()

    def next(self, instance):
        print('The button <next> is being pressed')
        ####SAVE!!!####

        # Set current dialogue utterance index to 0
        self.model.current_dialogue.set_current_utt(0)

        print("Index before: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)
        # Increment dialogue
        self.model.inc_current_dialogue()
        print("Index after: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)

        # Update dialogue view
        self.update_dialogue()

    def add_ap_label(self, instance):
        print('The button <%s> is being pressed' % instance.text)

        # Get the selected utterance
        utterance = self.model.current_dialogue.current_utterance
        utterance.set_ap_label(instance.text)

        # Update dialogue view
        self.update_dialogue(self.model.current_dialogue.utterance_index)

    def add_da_label(self, instance):
        print('The button <%s> is being pressed' % instance.text)

        # Get the selected utterance
        utterance = self.model.current_dialogue.current_utterance
        utterance.set_da_label(instance.text)

        # Update dialogue view
        self.update_dialogue(self.model.current_dialogue.utterance_index)
