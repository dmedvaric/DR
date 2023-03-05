from models import Setting

default_settings = {
    "movingStyle": {
        "description": "Method used to move the object, value type is string 'buttons' or 'gesture'",
        "default_value": "buttons",
    },
    "rotationStyle": {
        "description": "Method used to rotate the object, value type is string 'buttons' or 'gesture'",
        "default_value": "buttons",
    },
    "resizeStyle": {
        "description": "Method used to resize the object, value type is string 'buttons' or 'gesture'",
        "default_value": "buttons",
    },
    "textFont": {
        "description": "Font used in application, value type is string for example 'Roboto'",
        "default_value": "Roboto",
    },
    "textScale": {
        "description": "Scale used to change font size, value type is float 0.01-1.0",
        "default_value": "1.0",
    },
    "freezeEnabled": {
        "description": "Flag indicating if freeze feature is enabled. Values are 'True' or 'False'.",
        "default_value": "False",
    },
}

def construct_default_setting(name):
    return Setting(
        settingDesc = default_settings[name]["description"],
        settingName = name,
        settingValue = default_settings[name]["default_value"],
    )

def construct_setting_with_value(name, value):
    return Setting(
        settingDesc = default_settings[name]["description"],
        settingName = name,
        settingValue = value,
    )

def construct_default_settings_list():
    settings = []
    for setting_name in default_settings.keys():
        settings.append(construct_default_setting(setting_name))
    return settings

level_number_to_rating_label_mapping = {
    "1": "tap",
    "2": "gesture-move",
    "3": "button-move",
    "4": "gesture-scale",
    "5": "button-scale",
    "6": "choice-move",
    "7": "gesture-rotate",
    "8": "button-rotate",
    "9": "choice-interactions",
}   
