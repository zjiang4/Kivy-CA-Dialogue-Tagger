import utilities as utils
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from dialogue_model import Utterance, Dialogue, DialogueModel

data_path = "data/"
file_name = "train"
da_labels_file = "da_labels.txt"
ap_labels_file = "ap_labels.txt"


class Controller:

    def __init__(self):
        self.model = self.load()

    def menu(self, instance):
        print('The button <menu> is being pressed')

    def load(self):

        # Load JSON file
        data = utils.load_data(data_path, file_name)

        # Load labels
        da_labels = utils.load_labels(data_path, da_labels_file)
        ap_labels = utils.load_labels(data_path, ap_labels_file)

        # Loop over the dialogues and utterances in the data
        dialogues = []
        for dialogue in data['dialogues']:

            utterances = []
            for utterance in dialogue['utterances']:

                # Create a new utterance
                tmp_utterance = Utterance(utterance['text'], utterance['speaker'])

                # Set utterance labels if not blank
                if utterance['ap_label'] is not "":
                    tmp_utterance.set_ap_label(utterance['ap_label'])
                if utterance['da_label'] is not "":
                    tmp_utterance.set_da_label(utterance['da_label'])

                # Add to utterance list
                utterances.append(tmp_utterance)

            # Create a new dialogue with the utterances
            dialogues.append(Dialogue(dialogue['id'], utterances))

        # Create the dialogue model
        model = DialogueModel(data['dataset'], ap_labels, da_labels, dialogues)

        return model

    def save(self, instance):
        print('The button <save> is being pressed')

        # Holds the save data
        save_data = dict()

        # Loop over the dialogues and utterances in the model
        dialogues = []
        for dialogue in self.model.dialogues:

            tmp_dialogue = dict()

            utterances = []
            for utterance in dialogue.utterances:

                tmp_utterance = dict()

                # Add speaker, text and labels to utterance
                tmp_utterance['speaker'] = utterance.speaker
                tmp_utterance['text'] = utterance.text
                tmp_utterance['ap_label'] = utterance.ap_label
                tmp_utterance['da_label'] = utterance.da_label

                # Add to utterance list
                utterances.append(tmp_utterance)

            # Add id, number of utterances and utterance to dialogue
            tmp_dialogue['id'] = dialogue.id
            tmp_dialogue['num_utterances'] = dialogue.num_utterances
            tmp_dialogue['utterances'] = utterances

            # Add to dialogue list
            dialogues.append(tmp_dialogue)

        # Add dataset name and dialogues to save data
        save_data['dataset'] = self.model.dataset
        save_data['num_dialogues'] = self.model.num_dialogues
        save_data['dialogues'] = dialogues

        # Save data to file
        utils.save_data(data_path, file_name, save_data)

    def reset(self, instance):
        print('The button <refresh> is being pressed')

        # Get the current dialogue and clear the labels
        self.model.current_dialogue.clear_labels()

        # Update dialogue_box
        self.update_dialogue(self.model.current_dialogue.utterance_index)

    def toggle_mode(self, instance):
        print('The button <toggle> is being pressed')

        # If mode change is successful update dialogue_box
        if self.model.change_mode():
            self.update_dialogue()
        # Else make sure toggle button does not change state
        else:
            if instance.state == 'normal':
                instance.state = 'down'
            elif instance.state == 'down':
                instance.state = 'normal'

    def update_dialogue(self, selected_id=0):

        # Get the dialogue_box and call update function
        app = App.get_running_app()
        dialogue_box = app.root.get_widget('dialogue_box')
        dialogue_box.display_dialogue(self.model.current_dialogue, selected_id)

    def set_selected_utt(self, instance):

        # Get the selected utterance button
        buttons = ToggleButton.get_widgets('utterances')

        # If button is currently selected then re-select
        if instance.state == 'normal':
            instance.state = 'down'

        for btn in buttons:
            if btn.state == 'down':
                # Set the corresponding utterance as selected in the model
                self.model.current_dialogue.set_current_utt(int(btn.id))
                print("Selected utterance index: " + btn.id + " Utt: " + btn.text)

    def prev(self, instance):
        print('The button <prev> is being pressed')

        print("Index before: " + str(self.model.dialogue_index) + " ID: " + self.model.current_dialogue.id)
        # Decrement dialogue and if successful update dialogue_box
        if self.model.dec_current_dialogue():
            print("Index after: " + str(self.model.dialogue_index) + " ID: " + self.model.current_dialogue.id)
            self.update_dialogue(self.model.current_dialogue.utterance_index)

    def next(self, instance):
        print('The button <next> is being pressed')

        print("Index before: " + str(self.model.dialogue_index) + " ID: " + self.model.current_dialogue.id)
        # Increment dialogue and if successful update dialogue_box
        if self.model.inc_current_dialogue():
            print("Index after: " + str(self.model.dialogue_index) + " ID: " + self.model.current_dialogue.id)
            self.update_dialogue(self.model.current_dialogue.utterance_index)

    def add_label(self, instance):
        print('The button <%s> is being pressed' % instance.text)

        # Get the current utterance
        utterance = self.model.current_dialogue.current_utterance
        # Determine button set and set the label for the selected utterance
        if 'btn_bar_a' in instance.id:
            utterance.set_ap_label(instance.text)
        elif 'btn_bar_b' in instance.id:
            utterance.set_da_label(instance.text)

        # Get the current dialogue
        dialogue = self.model.current_dialogue
        # If the utterance is labeled and there are still some in the list
        if utterance.is_labeled and dialogue.utterance_index + 1 < dialogue.num_utterances:
            # Increment current utterance and update dialogue_box
            dialogue.set_current_utt(dialogue.utterance_index + 1)
            self.update_dialogue(dialogue.utterance_index)
        # Else just update dialogue_box
        else:
            self.update_dialogue(dialogue.utterance_index)

