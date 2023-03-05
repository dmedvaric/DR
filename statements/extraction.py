from models import IncompleteXapiStatementError
from utils import safeget
from settings.default import level_number_to_rating_label_mapping


def get_latest_finished_sessions_by_username(statements):
    res = list(
        filter(
            lambda s:
            safeget(s, "object", "id") == "http://usluge.ict-aac.hr/analiticARka/finish" and
            safeget(s, "verb", "id") == "http://adlnet.gov/expapi/verbs/terminated",
            statements
        )
    )

    if not res:
        return None

    usernames = set()
    statements_by_sessions = {}

    for r in res:
        username = safeget(r, "actor", "name")
        if username not in usernames:
            openid = safeget(r, "actor", "openid")
            if openid:
                statements_by_sessions[(username, openid)] = list(filter(
                    lambda s:
                    safeget(s, "actor", "openid") == openid,
                    statements
                ))
                usernames.add(username)

    return statements_by_sessions


def get_latest_finished_session(statements):
    res = list(
        filter(
            lambda s:
            safeget(s, "object", "id") == "http://usluge.ict-aac.hr/analiticARka/finish" and
            safeget(s, "verb", "id") == "http://adlnet.gov/expapi/verbs/terminated",
            statements
        )
    )

    if res:
        for r in res:
            try:
                session_openid = r["actor"]["openid"]
                break
            except (KeyError, TypeError, IndexError):
                continue

    else:
        return None

    if session_openid:
        return session_openid
    else:
        return None


def get_completed_level_stats(statements, level_number):
    rating_label = level_number_to_rating_label_mapping.get(str(level_number))
    level_rating = list(
        filter(
            lambda s:
            safeget(s, "object", "id") == f"http://usluge.ict-aac.hr/analiticARka/rating/interaction/{rating_label}" and
            safeget(s, "verb", "id") == "https://w3id.org/xapi/dod-isd/verbs/assessed",
            statements
        )
    )

    try:
        rating = int(level_rating[0]["result"]["score"]["raw"])
    except:
        rating = None

    level_res = list(
        filter(
            lambda s:
            safeget(s, "object", "id") == f"http://usluge.ict-aac.hr/analiticARka/level/{level_number}" and
            safeget(s, "verb", "id") == "https://w3id.org/xapi/dod-isd/verbs/completed",
            statements
        )
    )

    try:
        duration = float(level_res[0]["result"]["duration"][2:-1])
        skipped = level_res[0]["result"]["extensions"][
            "http://usluge.ict-aac.hr/analiticarka/result-extensions/skipped"]
        skipped = True if skipped == "True" else False
    except:
        raise IncompleteXapiStatementError

    return duration, skipped, rating
