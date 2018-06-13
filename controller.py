from kivy.uix.togglebutton import ToggleButton
from model import Model, Dialogue, Utterance


class Controller:

    def __init__(self):
        model = Model()
        self.model = model

    def add_label(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        buttons = ToggleButton.get_widgets('dialogue')
        for btn in buttons:
            if btn.state == 'down':
                print(btn.text)

    def prev(self, instance):
        print('The button <prev> is being pressed')
        ####SAVE!!!####


        print("Index before: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)
        # Decrement dialogue index or wrap to end
        if self.model.dialogue_index - 1 < 0:
            self.model.dialogue_index = self.model.num_dialogues - 1
        else:
            self.model.dialogue_index -= 1

        # Set new current dialogue with index
        self.model.current_dialogue = self.model.dialogues[self.model.dialogue_index]
        print("Index after: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)

        # Get dialogue box and call update function
        dialogue_box = instance.parent.ids['dialogue_box']
        dialogue_box.display_dialogue(self.model.current_dialogue)

    def next(self, instance):
        print('The button <next> is being pressed')
        ####SAVE!!!####


        print("Index before: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)
        # Increment dialogue index or wrpa to beginning
        if self.model.dialogue_index + 1 < self.model.num_dialogues:
            self.model.dialogue_index += 1
        else:
            self.model.dialogue_index = 0

        # Set new current dialogue with index
        self.model.current_dialogue = self.model.dialogues[self.model.dialogue_index]
        print("Index after: " + str(self.model.dialogue_index) + " File Name: " + self.model.current_dialogue.name)

        # Get dialogue box and call update function
        dialogue_box = instance.parent.ids['dialogue_box']
        dialogue_box.display_dialogue(self.model.current_dialogue)


