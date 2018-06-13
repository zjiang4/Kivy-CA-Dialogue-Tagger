from os import listdir

da_labels_path = "resources/da_labels.txt"
ap_labels_path = "resources/ap_labels.txt"
data_path = "data/"


class Model:
    def __init__(self):
        self.ap_labels = self.load_labels(ap_labels_path)
        self.da_labels = self.load_labels(da_labels_path)
        self.dialogues = self.load_text_data(data_path)
        self.dialogue_index = 0
        self.current_dialogue = self.dialogues[self.dialogue_index]
        self.num_dialogues = len(self.dialogues)

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

            dialogue = Dialogue(file_list[i])
            for line in text:
                utterance = Utterance(line)
                dialogue.add_utterance(utterance)

            dialogues.append(dialogue)

        return dialogues


class Dialogue:

    def __init__(self, name):
        self.name = name
        self.utterances = []
        self.utterance_index = None
        self.current_utterance = None

    def add_utterance(self, utterance):
        self.utterances.append(utterance)


class Utterance:

    def __init__(self, text):
        self.text = text
        self.ap_label = None
        self.da_label = None