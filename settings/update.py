from settings.default import construct_default_settings_list, construct_default_setting, default_settings
from models import IncompleteXapiStatementError, User
from statements.analytics import determine_preferred_interaction_style, get_app_settings_changes
from config_loader import config


def determine_new_settings(statements):
    new_settings = []

    new_settings.append(determine_preferred_interaction_style(statements, "movingStyle", 2, 3))
    new_settings.append(determine_preferred_interaction_style(statements, "resizeStyle", 4, 5))
    new_settings.append(determine_preferred_interaction_style(statements, "rotationStyle", 7, 8))

    changes = get_app_settings_changes(statements)
    for c in changes:
        new_settings.append(c)

    return new_settings


def merge_with_previous_settings(previous_settings, new_settings):
    for new_setting in new_settings:
        updated_previous = False
        for prev_setting in previous_settings:
            if prev_setting.settingName == new_setting.settingName:
                prev_setting.settingValue = new_setting.settingValue
                updated_previous = True

        if not updated_previous:
            previous_settings.append(new_setting)

    return previous_settings


def add_default_settings_if_missing(settings):
    settings_names = set({s.settingName for s in settings})
    default_settings_names = set(default_settings.keys())

    missing = default_settings_names - settings_names

    for setting_name in missing:
        settings.append(construct_default_setting(setting_name))

    return settings


def update_settings(statements, existing_user_record, username, update_timestamp):
    if statements:
        try:
            new_settings = determine_new_settings(statements)
        except IncompleteXapiStatementError:
            new_settings = None
    else:
        new_settings = None

    if existing_user_record:
        if not new_settings:
            # print("no new settings, returning existing user record")
            return existing_user_record

        prev_settings = User.settings.to_python(existing_user_record.settings)
        new_settings = merge_with_previous_settings(prev_settings, new_settings)
        new_settings = add_default_settings_if_missing(new_settings)

        existing_user_record.settings.update(settings=new_settings)
        existing_user_record.update(lastUpdateTime=update_timestamp)
        existing_user_record.save()

        # print("existing user record updated")
        return existing_user_record

    else:
        default_settings = construct_default_settings_list()

        if new_settings:
            # print("created new user and determined settings")
            settings = merge_with_previous_settings(default_settings, new_settings)
        else:
            # print("created new user with only default settings")
            settings = default_settings

        if new_settings or config.RETURN_AND_SAVE_DEFAULT_SETTINGS_IF_NO_RECORDS_FOUND:
            new_user = User(
                userId=username,
                lastUpdateTime=update_timestamp,
                settings=settings,
            )
            User.save(new_user)
            return new_user
        else:
            return None
