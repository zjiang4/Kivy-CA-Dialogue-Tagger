class DialogueModel:
    def __init__(self, dataset, ap_labels, da_labels, dialogues):

        # Load default data
        self.dataset = dataset
        self.ap_labels = ap_labels
        self.da_labels = da_labels
        # All dialogues
        self.dialogues = dialogues
        self.num_dialogues = len(self.dialogues)
        # Labeled and unlabeled
        self.labeled_dialogues = []
        self.unlabeled_dialogues = []
        self.num_labeled = len(self.labeled_dialogues)
        self.num_unlabeled = len(self.unlabeled_dialogues)
        # Default current dialogue
        self.dialogue_index = 0
        self.current_dialogue = self.dialogues[self.dialogue_index]

        # Split into labeled and unlabeled
        self.get_dialogues_states()

        # Set current mode
        if self.num_unlabeled > 0:
            self.unlabeled_mode = True
        else:
            self.unlabeled_mode = False

        # Set current dialogue
        self.set_current_dialogue(self.dialogue_index)

    def set_current_dialogue(self, index):

        # Check mode has some in the list and index is within range
        if self.unlabeled_mode and self.num_unlabeled > 0:
            if self.num_unlabeled > index >= 0:
                self.dialogue_index = index
                self.current_dialogue = self.unlabeled_dialogues[self.dialogue_index]
            return True

        elif not self.unlabeled_mode and self.num_labeled > 0:
            if self.num_labeled > index >= 0:
                self.dialogue_index = index
                self.current_dialogue = self.labeled_dialogues[self.dialogue_index]
            return True

        return False

    def get_dialogues_states(self):

        # Reset labeled and unlabeled lists
        self.labeled_dialogues = []
        self.unlabeled_dialogues = []

        # Split dialogues into lists
        for dialogue in self.dialogues:

            if dialogue.check_labels():
                self.labeled_dialogues.append(dialogue)
            else:
                self.unlabeled_dialogues.append(dialogue)

        # Set number of labeled and unlabeled
        self.num_labeled = len(self.labeled_dialogues)
        self.num_unlabeled = len(self.unlabeled_dialogues)

    def change_mode(self):

        # Update the current lists
        self.get_dialogues_states()

        # Change mode if there are dialogues in the list to change to
        if self.unlabeled_mode and self.num_labeled > 0:
            self.unlabeled_mode = False
            return self.set_current_dialogue(0)

        elif not self.unlabeled_mode and self.num_unlabeled > 0:
            self.unlabeled_mode = True
            return self.set_current_dialogue(0)

        return False

    def inc_current_dialogue(self):

        # Get number of dialogues in the current set
        if self.unlabeled_mode:
            num_dialogues = self.num_unlabeled
        else:
            num_dialogues = self.num_labeled

        # If there is one or less dialogues do nothing
        if num_dialogues == 0:
            return False
        else:
            # Increment dialogue index or wrap to beginning
            if self.dialogue_index + 1 < num_dialogues:
                self.dialogue_index += 1
            else:
                self.dialogue_index = 0

            # Set new current dialogue with index
            self.set_current_dialogue(self.dialogue_index)

            # Only change current utterance if this isn't the last dialogue
            if num_dialogues > 1:
                # Set new current dialogue index to 0
                self.current_dialogue.set_current_utt(0)

        # Update the current lists
        self.get_dialogues_states()

        return True

    def dec_current_dialogue(self):

        # Update the current lists
        self.get_dialogues_states()

        # Get number of dialogues in the current set
        if self.unlabeled_mode:
            num_dialogues = self.num_unlabeled
        else:
            num_dialogues = self.num_labeled

        # If there is one or less dialogues do nothing
        if num_dialogues == 0:
            return False
        else:
            # Decrement dialogue index or wrap to end
            if self.dialogue_index - 1 < 0:
                self.dialogue_index = num_dialogues - 1
            else:
                self.dialogue_index -= 1

            # Set new current dialogue with index
            self.set_current_dialogue(self.dialogue_index)

            # Only change current utterance if this isn't the last dialogue
            if num_dialogues > 1:
                # Set new current dialogue index to 0
                self.current_dialogue.set_current_utt(0)

            return True


class Dialogue:

    def __init__(self, dialogue_id, utterances):
        self.dialogue_id = dialogue_id
        self.utterances = utterances
        self.num_utterances = len(self.utterances)
        self.utterance_index = 0
        self.current_utterance = self.utterances[0]
        self.is_labeled = False
        self.check_labels()

    def set_current_utt(self, index):
        self.utterance_index = index
        self.current_utterance = self.utterances[self.utterance_index]

    def set_utterances(self, utterances):

        # Replace utterances
        self.utterances = utterances
        self.num_utterances = len(self.utterances)

        # Reset current utterance to 0
        self.set_current_utt(0)

        # Check labels
        self.check_labels()

    def clear_labels(self):

        # Set utterances to default labels
        for utt in self.utterances:
            utt.clear_ap_label()
            utt.clear_da_label()

    def check_labels(self):

        # Check if any utterances still have default labels
        for utt in self.utterances:

            if not utt.check_labels():
                self.is_labeled = False
                return self.is_labeled

        self.is_labeled = True
        return self.is_labeled


class Utterance:
    def __init__(self, text, speaker='', ap_label='AP-Label', da_label='DA-Label'):
        self.text = text
        self.speaker = speaker
        self.ap_label = ap_label
        self.da_label = da_label
        self.is_labeled = False

    def set_ap_label(self, label):
        self.ap_label = label
        self.check_labels()

    def set_da_label(self, label):
        self.da_label = label
        self.check_labels()

    def clear_ap_label(self):
        self.set_ap_label('AP-Label')

    def clear_da_label(self):
        self.set_da_label('DA-Label')

    def check_labels(self):

        # Check if utterance still has default labels
        if self.ap_label == 'AP-Label' or self.da_label == 'DA-Label':
            self.is_labeled = False
            return self.is_labeled

        self.is_labeled = True
        return self.is_labeled
