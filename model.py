from os import listdir

da_labels_path = "resources/da_labels.txt"
ap_labels_path = "resources/ap_labels.txt"
data_path = "data/"


class Model:
    def __init__(self):
        self.ap_labels = self.load_labels(ap_labels_path)
        self.da_labels = self.load_labels(da_labels_path)
        self.dialogues = self.load_text_data(data_path)
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

    def load_labels(self, path):

        with open(path) as file:
            labels = [line.rstrip() for line in file]

        return labels

    def load_text_data(self, path):

        file_list = listdir(path)
        dialogues = []

        for i in range(len(file_list)):

            with open(path + file_list[i]) as file:
                text = [line.rstrip() for line in file]

            utterances = []
            for line in text:
                utterances.append(Utterance(line))

            dialogue = Dialogue(file_list[i], utterances)
            dialogues.append(dialogue)

        return dialogues


class Dialogue:

    def __init__(self, name, utterances):
        self.name = name
        self.utterances = utterances
        self.utterance_index = 0
        self.current_utterance = self.utterances[0]

    def set_current_utt(self, index):
        self.utterance_index = index
        self.current_utterance = self.utterances[self.utterance_index]


class Utterance:
    def __init__(self, text):
        self.speaker = None
        self.text = text
        self.ap_label = 'AP Label'
        self.da_label = 'DA Label'

    def set_ap_label(self, label):
        self.ap_label = label

    def set_da_label(self, label):
        self.da_label = label