from os import listdir

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton

from model import Model, Dialogue, Utterance

da_labels_path = "resources/da_labels.txt"
ap_labels_path = "resources/ap_labels.txt"
data_path = "data/"


class Controller():

    def __init__(self):
        model = Model()
        model.ap_labels = load_labels(ap_labels_path)
        model.da_labels = load_labels(da_labels_path)
        model.dialogues = load_text_data(data_path)
        model.dialogue_index = 0
        model.current_dialogue = model.dialogues[model.dialogue_index]
        model.num_dialogues = len(model.dialogues)

        self.model = model



    def add_label(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        buttons = ToggleButton.get_widgets('utt')
        for btn in buttons:
            if btn.state == 'down':
                print(btn.text)

    def next_prev(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        self.model.dialogue_index += 1
        self.model.current_dialogue = self.model.dialogues[self.model.dialogue_index]
        # for utt in self.model.current_dialogue.utterances:
        #     print(utt.text)


def load_labels(path):

    with open(path) as file:
        labels = [line.rstrip() for line in file]

    return labels

def load_text_data(path):

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
