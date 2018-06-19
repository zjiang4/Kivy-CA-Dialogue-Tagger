
class DialogueModel:
    def __init__(self, dataset, ap_labels, da_labels, dialogues):
        self.dataset = dataset
        self.ap_labels = ap_labels
        self.da_labels = da_labels
        self.dialogues = dialogues
        self.num_dialogues = len(self.dialogues)
        self.dialogue_index = 0
        self.current_dialogue = self.dialogues[0]

    def set_current_dialogue(self, index):
        self.dialogue_index = index
        self.current_dialogue = self.dialogues[self.dialogue_index]

    def inc_current_dialogue(self):

        # Increment dialogue index or wrap to beginning
        if self.dialogue_index + 1 < self.num_dialogues:
            self.dialogue_index += 1
        else:
            self.dialogue_index = 0

        # Set new current dialogue with index
        self.set_current_dialogue(self.dialogue_index)

    def dec_current_dialogue(self):

        # Decrement dialogue index or wrap to end
        if self.dialogue_index - 1 < 0:
            self.dialogue_index = self.num_dialogues - 1
        else:
            self.dialogue_index -= 1

        # Set new current dialogue with index
        self.set_current_dialogue(self.dialogue_index)


class Dialogue:

    def __init__(self, id, utterances):
        self.id = id
        self.utterances = utterances
        self.num_utterances = len(self.utterances)
        self.utterance_index = 0
        self.current_utterance = self.utterances[0]

    def set_current_utt(self, index):
        self.utterance_index = index
        self.current_utterance = self.utterances[self.utterance_index]


class Utterance:
    def __init__(self, text, speaker='', ap_label='AP Label', da_label='DA Label'):
        self.text = text
        self.speaker = speaker
        self.ap_label = ap_label
        self.da_label = da_label

    def set_ap_label(self, label):
        self.ap_label = label

    def set_da_label(self, label):
        self.da_label = label
