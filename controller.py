from kivy.clock import Clock
import utilities as utils
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from dialogue_model import Utterance, Dialogue, DialogueModel

data_path = "data/"
file_name = "kvret_train_set"
da_labels_file = "da_labels.txt"
ap_labels_file = "ap_labels.txt"


class Controller:

    def __init__(self):
        self.model = self.load()

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

                # Set the slots if they exist
                if 'slots' in utterance:
                    tmp_utterance.slots = utterance['slots']

                # Add to utterance list
                utterances.append(tmp_utterance)

            # Create a new dialogue with the utterances
            dialogues.append(Dialogue(dialogue['dialogue_id'], utterances, dialogue['scenario']))

        # Create the dialogue model
        model = DialogueModel(data['dataset'], ap_labels, da_labels, dialogues)

        return model

    def save(self):

        # Holds the save data
        save_data = dict()

        # Loop over the dialogues and utterances in the model
        dialogues = []
        dialogue_index = 0
        for dialogue in self.model.dialogues:

            tmp_dialogue = dict()
            dialogue_index += 1

            utterances = []
            for utterance in dialogue.utterances:

                tmp_utterance = dict()

                # Add speaker, text and labels to utterance
                tmp_utterance['speaker'] = utterance.speaker
                tmp_utterance['text'] = utterance.text
                tmp_utterance['ap_label'] = utterance.ap_label
                tmp_utterance['da_label'] = utterance.da_label

                # Add slots to utterance if they exist
                if utterance.slots is not None:
                    tmp_utterance['slots'] = utterance.slots

                # Add to utterance list
                utterances.append(tmp_utterance)

            # Add id, number of utterances, utterance and scenario to dialogue
            tmp_dialogue['dialogue_id'] = self.model.dataset + "_" + str(dialogue_index)
            tmp_dialogue['num_utterances'] = dialogue.num_utterances
            tmp_dialogue['utterances'] = utterances
            tmp_dialogue['scenario'] = dialogue.scenario

            # Add to dialogue list
            dialogues.append(tmp_dialogue)

        # Add dataset name and dialogues to save data
        save_data['dataset'] = self.model.dataset
        save_data['num_dialogues'] = self.model.num_dialogues
        save_data['dialogues'] = dialogues

        # Save data to file
        utils.save_data(data_path, file_name, save_data)

    def menu(self, instance):
        print('The button <menu> is being pressed')

    def open_file(self, instance):
        print('The button <open> is being pressed')

    def save_file_as(self, instance):
        print('The button <save_as> is being pressed')

    def save_file(self, instance):
        print('The button <save_file> is being pressed')
        # Delay call to save function so it doesn't interrupt button
        Clock.schedule_once(lambda dt: self.save(), 0.5)

    def refresh(self, instance):
        print('The button <refresh> is being pressed')

        # Load JSON file
        data = utils.load_data(data_path, file_name)

        # Get the current dialogues id
        target_id = self.model.current_dialogue.dialogue_id

        # Loop over the dialogues and utterances in the data
        for dialogue in data['dialogues']:

            # If the id's match get the utterances
            if dialogue['dialogue_id'] == target_id:

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

                # Update current dialogue with the utterances
                self.model.current_dialogue.set_utterances(utterances)
                break

        # Update dialogue_box
        self.update_dialogue()

    def delete(self, instance):
        print('The button <delete> is being pressed')

        # Delete the current dialogue from the list
        self.model.delete_current_dialogue()

        # Update dialogue_box and stats
        self.update_dialogue(self.model.current_dialogue.utterance_index)
        self.update_stats()

    def clear(self, instance):
        print('The button <clear> is being pressed')

        # Get the current dialogue and clear the labels
        self.model.current_dialogue.clear_labels()

        # Update dialogue_box
        self.update_dialogue(self.model.current_dialogue.utterance_index)

    def toggle_mode(self, instance):
        print('The button <toggle> is being pressed')

        # If mode change is successful update dialogue_box and stats
        if self.model.change_mode():
            # Set the current dialogue index to 0
            self.model.current_dialogue.set_current_utt(0)
            self.update_dialogue()
            self.update_stats()
        # Else make sure toggle button does not change state
        else:
            if instance.state == 'normal':
                instance.state = 'down'
            elif instance.state == 'down':
                instance.state = 'normal'

    def get_mode(self):

        # Get the current mode of the model
        return self.model.unlabeled_mode

    def get_current_stats(self):

        # Get the current dialogue id
        dialogue_id = self.get_current_dialogue().dialogue_id

        # Get number of labeled/unlabeled and total dialogues
        labeled = self.model.num_labeled
        unlabeled = self.model.num_unlabeled
        total = self.model.num_dialogues
        return dialogue_id, labeled, unlabeled, total

    def update_stats(self):

        # Get the menu_bar and call update function
        app = App.get_running_app()
        menu_bar = app.root.get_widget('menu_bar')
        menu_bar.display_stats(*self.get_current_stats())

    def get_current_dialogue(self):
        return self.model.current_dialogue

    def update_dialogue(self, selected_id=0):

        # Get the dialogue_box and call update function
        app = App.get_running_app()
        dialogue_box = app.root.get_widget('dialogue_box')
        dialogue_box.display_dialogue(self.get_current_dialogue(), selected_id)

    def set_selected_utt(self, instance):

        # Get the selected utterance button
        buttons = ToggleButton.get_widgets('utterances')

        for btn in buttons:
            if btn.state == 'down':
                # Set the corresponding utterance as selected in the model
                self.get_current_dialogue().set_current_utt(int(btn.id))
                print("Selected utterance index: " + btn.id + " Utt: " + btn.text)

    def next(self, instance):
        print('The button <next> is being pressed')

        print("Index before: " + str(self.model.dialogue_index) + " ID: " + self.get_current_dialogue().dialogue_id)
        # Increment dialogue and if successful update dialogue_box and stats
        if self.model.inc_current_dialogue():
            print("Index after: " + str(self.model.dialogue_index) + " ID: " + self.get_current_dialogue().dialogue_id)
            self.update_dialogue(self.get_current_dialogue().utterance_index)
            self.update_stats()
        else:
            # Display default
            self.update_dialogue(self.get_current_dialogue())
            self.update_stats()

    def prev(self, instance):
        print('The button <prev> is being pressed')

        print("Index before: " + str(self.model.dialogue_index) + " ID: " + self.get_current_dialogue().dialogue_id)
        # Decrement dialogue and if successful update dialogue_box and stats
        if self.model.dec_current_dialogue():
            print("Index after: " + str(self.model.dialogue_index) + " ID: " + self.get_current_dialogue().dialogue_id)
            self.update_dialogue(self.get_current_dialogue().utterance_index)
            self.update_stats()
        else:
            # Display default
            self.update_dialogue(self.get_current_dialogue())
            self.update_stats()

    def get_ap_labels(self):
        return self.model.ap_labels

    def get_da_labels(self):
        return self.model.da_labels

    def add_label(self, instance):
        print('The button <%s> is being pressed' % instance.text)

        # Get the current dialogue and utterance
        dialogue = self.get_current_dialogue()
        utterance = dialogue.current_utterance

        # Determine button set and set the label for the selected utterance
        if 'btn_bar_a' in instance.id:
            utterance.set_ap_label(instance.text)
        elif 'btn_bar_b' in instance.id:
            utterance.set_da_label(instance.text)

        # If the utterance is labeled and there are still some in the list
        if utterance.is_labeled and dialogue.utterance_index + 1 < dialogue.num_utterances:
            # Increment current utterance and update dialogue_box
            dialogue.set_current_utt(dialogue.utterance_index + 1)
            self.update_dialogue(dialogue.utterance_index)
        # Else just update dialogue_box
        else:
            self.update_dialogue(dialogue.utterance_index)

