
da_labels_path = "resources/da_labels.txt"
ap_labels_path = "resources/ap_labels.txt"


def load_labels(path):

    with open(path) as file:
        labels = [line.rstrip() for line in file]

    return labels

def callback(instance):
    print('The button <%s> is being pressed' % instance.text)