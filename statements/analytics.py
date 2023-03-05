from utils import safeget
from fnmatch import fnmatch
from settings.default import construct_default_setting, construct_setting_with_value
from statements.extraction import get_completed_level_stats

def get_app_settings_changes(statements):
    res = list(sorted(
            filter(
                lambda s: 
                    fnmatch(str(safeget(s, "object", "id") or ''), "http://usluge.ict-aac.hr/analiticARka/level/*/settings") and
                    safeget(s, "verb", "id") == "https://w3id.org/xapi/seriousgames/verbs/pressed",
                statements
            ),
            key = lambda s: s.get("timestamp"), reverse=True
    ))

    changed_app_settings = []

    if res:
        used_font = safeget(res[0], "result", "extensions", "http://usluge.ict-aac.hr/analiticarka/result-extensions/used-font")
        text_size = safeget(res[0], "result", "extensions", "http://usluge.ict-aac.hr/analiticarka/result-extensions/text-size")
        freeze_enabled = safeget(res[0], "result", "extensions", "http://usluge.ict-aac.hr/analiticarka/result-extensions/freeze-enabled")

        if used_font:
            changed_app_settings.append(construct_setting_with_value("textFont", used_font))
        if text_size:
            changed_app_settings.append(construct_setting_with_value("textScale", text_size))
        if freeze_enabled:
            changed_app_settings.append(construct_setting_with_value("freezeEnabled", freeze_enabled))
    
    # remove None values
    changed_app_settings = [x for x in changed_app_settings if x]

    return changed_app_settings


# level_buttons => level with buttons interaction
# level_gesture => level with gesture interaction
def determine_preferred_interaction_style(statements, setting_name, level_gesture, level_buttons):
    duration_gst, skipped_gst, rating_gst = get_completed_level_stats(statements, level_gesture)
    duration_btn, skipped_btn, rating_btn = get_completed_level_stats(statements, level_buttons)

    if skipped_btn and skipped_gst:
        # print("skipped both levels")
        return construct_default_setting(setting_name)
    elif skipped_btn:
        # print("skipped btn level")
        return construct_setting_with_value(setting_name, "gesture")
    elif skipped_gst:
        # print("skipped gst level")
        return construct_setting_with_value(setting_name, "buttons")
    else:
        if rating_btn and rating_gst and rating_btn != rating_gst:
            # print("getting level with higher rating. gesture: ", rating_gst, " buttons: ", rating_btn)
            return construct_setting_with_value(setting_name, "gesture" if rating_gst > rating_btn else "buttons")
        else:
            if duration_btn == duration_gst:
                # print("default because of identical duration because durations are: ", duration_btn, duration_gst)
                return construct_default_setting(setting_name)
            else:
                # print("getting level with shorter duration because ratings are: ", rating_btn, rating_gst)
                return construct_setting_with_value(setting_name, "gesture" if duration_gst < duration_btn else "buttons")
