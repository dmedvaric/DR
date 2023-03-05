from main import app
import requests
import dateutil.parser
from auth import login_required
from config_loader import config
from models import User
from utils import safeget
from statements.extraction import get_latest_finished_session
from settings.update import update_settings
from datetime import datetime, timezone
from flask import jsonify

@app.route('/settings/refresh/user/<username>', methods=['GET'])
@login_required
def refresh_user_settings(username: str):
    run_time = datetime.now(tz=timezone.utc)

    update_time_filter = ""

    existing_user_record = User.objects(userId=username).first()
    if existing_user_record:
        last_update_time = existing_user_record.lastUpdateTime
        if last_update_time:
            update_time_filter = f"""
                ,
                "statement.timestamp": {{
                    "$gte": "{last_update_time.isoformat()}"
                }}
            """

    pipeline = f"""
    [
        {{"$match": 
            {{
                "statement.actor.name": "{username}"
                {update_time_filter}
            }}
        }},
        {{"$sort":
            {{
                "timestamp": -1
            }}
        }}
    ]
    """

    params = {'pipeline': pipeline}
    print(params)

    headers = {
        'Authorization': f'Basic {config.LRS_AUTH_BASIC_TOKEN}',
        'X-Experience-API-Version': '1.0.3',
    }

    response = requests.get(url=f"{config.LRS_URL}/api/statements/aggregate", headers=headers, params=params)
    response_json = response.json()

    statements = []
    for r in response_json:
        try:
            statements.append(r["statement"])
        except KeyError:
            continue

    for s in statements:
        s["timestamp"] = dateutil.parser.parse(s["timestamp"])
        s["stored"] = dateutil.parser.parse(s["stored"])
    
    openid = get_latest_finished_session(statements)
    if not openid:
        session_statements = None

    # get all statements from the session and sort by newest
    session_statements = list(sorted(
        filter(
            lambda s: safeget(s, "actor", "openid") == openid, 
            statements
        ),
        key = lambda s: s.get("timestamp"), reverse=True
    ))

    updated_settings = update_settings(session_statements, existing_user_record, username, run_time)

    if updated_settings:
        return jsonify(updated_settings)
    else:
        return "no records for that username", 404
