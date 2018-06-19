import json


def load_data(path, file_name):

    with open(path + file_name + ".json") as file:
        data = json.load(file)
    file.close()

    return data


def save_data(path, file_name, data):

    with open(path + file_name + '.json', 'w+') as file:
        json.dump(data, file, default=obj_to_json, sort_keys=False, indent=4, separators=(',', ': '))


def load_labels(path, file_name):

    with open(path + file_name) as file:
        labels = [line.rstrip() for line in file]
    file.close()

    return labels


def obj_to_json(obj):
    return obj.__dict__
