import json
import traceback
from dialogue_model import Utterance, Dialogue


def load_data(path, file_name):
    try:
        with open(path + file_name + ".json") as file:
            data = json.load(file)
        file.close()
    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return data


def load_dialogues(data):

    try:
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
            tmp_dialogue = Dialogue(dialogue['dialogue_id'], utterances)

            # Set the scenario if it exists
            if 'scenario' in dialogue:
                tmp_dialogue.scenario = dialogue['scenario']

            # Add to dialogue list
            dialogues.append(tmp_dialogue)

    except KeyError:
        traceback.print_exc()
        return False

    return dialogues


def save_data(path, file_name, data):

    with open(path + file_name + '.json', 'w+') as file:
        json.dump(data, file, default=obj_to_json, sort_keys=False, indent=4, separators=(',', ': '))


def load_labels(path, file_name):
    try:
        with open(path + file_name) as file:
            labels = [line.rstrip() for line in file]
        file.close()
    except (IOError, ValueError):
        traceback.print_exc()
        return False

    return labels


def obj_to_json(obj):
    return obj.__dict__
