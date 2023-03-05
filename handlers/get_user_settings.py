from datetime import datetime, timezone
from main import app
from auth import login_required
from models import User
from settings.default import construct_default_settings_list
from flask import jsonify
from config_loader import config

@app.route("/settings/get/user/<username>", methods=["GET",])
@login_required
def get_user_settings(username: str):
    user_record = User.objects(userId=username)

    if user_record:
        user_record = user_record
        print(user_record)
        return jsonify(user_record)
    

    elif config.RETURN_AND_SAVE_DEFAULT_SETTINGS_IF_NO_RECORDS_FOUND:
        new_user = User(
            userId = username,
            lastUpdateTime = datetime.now(tz=timezone.utc),
            settings = construct_default_settings_list()
        )

        User.save(new_user)
        user_record = new_user
        return jsonify(user_record)
    
    else:
        return "no records for that username", 404

