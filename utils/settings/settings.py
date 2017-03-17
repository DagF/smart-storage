import os
import json
from base64 import b64decode, b64encode

# settings
SETTINGS_FILE = os.path.dirname(os.path.realpath(__file__)) + '/settings.json'


def create_settings_dict(
        project="Nytt prosjekt",
        description="Beskrivelse",
        owner="navn",
        number="78778",
        type="prototype",
):
    return {
        "image": "",
        "project": project,
        "description": description,
        "name": owner,
        "number": number,
        "type": type,
    }


def get_values_from_settings(settings=create_settings_dict()):
    return {
        'number': settings.get("number"),
        'owner': settings.get("owner"),
        'project': settings.get("project"),
        'description': settings.get("description"),
        'type': settings.get("type"),
    }


def load_settings():
    try:
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
    except:
        save_settings(create_settings_dict())
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
    return get_values_from_settings(data)


def save_settings(values):
    if 'image' not in values:
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
            values['image'] = data['image']
    with open(SETTINGS_FILE, 'w') as outfile:
        json.dump(values, outfile)


def load_image_from_file(settings=create_settings_dict()):
    return b64decode(settings.get("image"))


def load_image():
    try:
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
    except:
        save_settings(create_settings_dict())
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
    return load_image_from_file(data)


def save_image(image):
    try:
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
    except:
        save_settings(create_settings_dict())
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
    data['image'] = b64encode(image.read())
    save_settings(data)
