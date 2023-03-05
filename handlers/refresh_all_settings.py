from datetime import datetime, timezone
from main import app
import dateutil.parser
from models import IncompleteXapiStatementError
from auth import login_required
from config_loader import config
import requests
from statements.extraction import get_latest_finished_sessions_by_username
from settings.update import update_settings
from models import User, RefreshRun


@app.route("/settings/refresh/all", methods=["GET", ])
@login_required
def refresh_all_settings():
    run_time = datetime.now(timezone.utc)

    last_run = RefreshRun.objects().order_by('-runTime').first()
    if last_run and last_run.runTime:
        params = {
            'since': last_run.runTime.isoformat(),
            # 'until': run_time,    This causes a bug where statements from the next page are not retrieved
        }
    else:
        params = {}

    headers = {
        'Authorization': f'Basic {config.LRS_AUTH_BASIC_TOKEN}',
        'X-Experience-API-Version': '1.0.3',
    }


    statements = []

    response = requests.get(url=f"{config.LRS_URL}/data/xAPI/statements", headers=headers, params=params)

    response_json = response.json()
    statements += response_json.get('statements')



    while response_json.get('more'):
        url = f"{config.LRS_URL}{response_json.get('more')}"

        response = requests.get(url=url, headers=headers)
        response_json = response.json()
        statements += response_json.get('statements')

    for s in statements:
        s["timestamp"] = dateutil.parser.parse(s["timestamp"])
        s["stored"] = dateutil.parser.parse(s["stored"])

    if not statements:
        return "no new statements", 200

    statements = list(sorted(statements, key=lambda s: s.get("timestamp"), reverse=True))

    statements_by_sessions = get_latest_finished_sessions_by_username(statements)

    if not statements_by_sessions:
        return "no new finished game sessions", 200

    updated_user_cnt = 0

    for (username, openid), session_statements in statements_by_sessions.items():

        existing_user_record = User.objects(userId=username).first()
        try:
            update_settings(session_statements, existing_user_record, username, run_time)
            updated_user_cnt += 1
        except IncompleteXapiStatementError:
            print(
                f"Encountered incomplete xAPI statements for user '{username}'. Skipping update to user '{username}'...")

    refresh_run = RefreshRun(
        runTime=run_time,
        updatedUserCount=updated_user_cnt,
    )
    RefreshRun.save(refresh_run)

    return f"updated settings for {updated_user_cnt} users", 200
