
class Model():
    def __init__(self):
        self.ap_labels = []
        self.da_labels = []
        self.dialogues = []
        self.dialogue_index = None
        self.current_dialogue = None
        self.num_dialogues = None


class Dialogue():

    def __init__(self, name):
        self.name = name
        self.utterances = []
        self.utterance_index = None
        self.current_utterance = None

    def add_utterance(self, utterance):
        self.utterances.append(utterance)

class Utterance():

    def __init__(self, text):
        self.text = text
        self.ap_label = None
        self.da_label = None