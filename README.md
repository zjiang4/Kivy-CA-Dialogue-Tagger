# Conversation Analysis Dialogue Tagger
Facilitates labelling of dialogues with Dialogue Acts (DA) and Adjacency Pairs (AP) to create *AP-types* 
that are closely aligned with the concept of typed AP in Conversation Analysis (CA).
A full explanation of the intended use for CA the labelled corpus can be found in the paper 
[Conversation Analysis Structured Dialogue for Multi-Domain Dialogue Management](https://sites.google.com/view/dexahai-18/home).
A definition of the DA and AP labels can be found in the [CA schema](Conversation%20Analysis%20Schema.md).

This software is written in Python 3.6 using the [Kivy library](https://kivy.org/#home).

<p align="center">
<img src="/resources/ca-tagger-screenshot.png">
</p>

## Usage
Currently input corpus data must be in the /data directory and filenames manually specified at the top of main.py.
DA and AP labels are specified in .txt files with one label per line. Dialogues must be in a .json file
in [this format](*Data-Foramt).

Currently the menu, open file and save-as buttons are not yet implemented.
![menu_btn](/resources/menu_black.png)![open_btn](/resources/open_black.png)![save_as_btn](/resources/save_as_black.png)

![save_btn](/resources/save_black.png) Saves __all__ dialogues in the current dataset to the .json file.
Changes made with the following 3 buttons are only written to file once this button is clicked.

![refresh_btn](/resources/refresh_black.png) Removes any changes to the __current__ dialogue since the last save.

![clear_btn](/resources/clear_black.png) Removes all labels from the __current__ dialogue.

![delete_btn](/resources/delete_black.png) Deletes __current__ dialogue from the dataset.

![labelled_btn](/resources/labelled_black.png) Toggles between labelled and unlabelled dialogues.
Dialogues are automatically added to the labelled set when all utterances have both DA and AP labels.

## Datasets
Two corpora are included in the /data directory with both training and test sets.
default.json will be loaded if no valid file is specified and test.json is for development.

[Key-Value Retrieval Networks for Task-Oriented Dialogue (KVRET)](https://nlp.stanford.edu/blog/a-new-multi-turn-multi-domain-task-oriented-dialogue-dataset/)
 which is labelled.

[Frames](https://datasets.maluuba.com/Frames) which is unlabelled.

## Data Format
The following is an example of the JSON format required for the input data.
Note that the 'slots' and 'scenario' objects are optional and are intended to allow the inclusion of additional data
that may be useful. They will be ignored if not present.

    {
        "dataset": "dataset_name",
        "num_dialogues": 1,
        "dialogues": [
            {
                "dialogue_id": "dataset_name_1",
                "num_utterances": 2,
                "utterances": [
                    {
                        "speaker": "A",
                        "text": "Utterance 1 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label"
                    },
                    {
                        "speaker": "B",
                        "text": "Utterance 2 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label",
                        "slots": { // Optional
                            "slot_name": "slot_value"
                        }
                    }
                ],
                "scenario": { //Optional
                    "db_id": "1",
                    "db_type": "i.e booking",
                    "task": "i.e book",
                    "items": []
                }
            }
        ]
    }

Button colour = 88, 88, 88
Button down colour = 50, 164, 206
# TODO
## Menu
- Menu? (export as plain text)
- Load functionality
- Save as
- Popup warning for delete dialogue
- Fit text to labels/labels to text?
- Tooltips https://gist.github.com/opqopq/15c707dc4cffc2b6455f

## Dialogue View
- Size of text btn/color of text 
- Background for labels/color of text
- Label clear button?
- Label edit?
- Label/button text wrap
- Speaker labels (remove colon in button labels)
- Scrollable?
- Edit utterance
- Delete utterance

## Button bars
- Group AP labels by type? Four boxes (FPPbase, SPPbase and None AP for example)
- Text/button colours?
- Highlight buttons for utterance labels? (Group/toggle buttons)
- Make labels generic (model, controller and view)??
- Resize bar to fit buttons

## Model

## MISC
- Size on smaller screen?
- De kivify?
- Documentation/readme
- DA and AP label instructions in readme
- Add datasets
- Popup for exit and saving
- Add Glowboards
- Different default/empty list method/dialogue?
- Handle no valid file to load/save


    ### EXAMPLE FOR DE-KIVY-FYING ###
    # CANVAS
    #     with self.canvas:  # Instead of Kivy?
    #         Color(53 / 255.0, 53 / 255.0, 53 / 255.0, 1)
    #         self.rect = Rectangle(source='resources/background.png', pos=self.pos, size=self.size)
    #     self.bind(pos=self.update_rect, size=self.update_rect)
    #
    # def update_rect(self, *args):# Instead of Kivy?
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size
    
    # IMAGE BUTTON
    # self.menu_btn_layout = AnchorLayout(anchor_x='center', anchor_y='center', width=50, size_hint=(None, 1))
    # self.menu_btn = Button(size=(40, 40))
    # self.menu_btn.bind(on_press=ctrl.menu)
    # self.menu_img = Image(source='resources/menu.png', height=40, width=40)
    # self.menu_btn_layout.add_widget(self.menu_btn)
    # self.menu_btn_layout.add_widget(self.menu_img)
