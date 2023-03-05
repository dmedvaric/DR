import os
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
from main import app


load_dotenv()


class Config:
    def __init__(self):
        # username:password
        #self.APP_CREDENTIALS = os.environ.get("APP_CREDENTIALS", "hotel:trivago")
        self.APP_CREDENTIALS = os.environ.get("APP_CREDENTIALS")


        #self.LRS_URL = os.environ.get("http://121.54.21.212")
        self.LRS_URL = os.environ.get("LRS_URL")
        self.LRS_AUTH_BASIC_TOKEN = os.environ.get("LRS_AUTH_BASIC_TOKEN")
        #self.LRS_AUTH_BASIC_TOKEN = os.environ.get("OWU5ODg2YWQyMzBiMTRhZj5ODg2YWQyM")

        #DB_URI = os.environ.get("mongodb+srv://username:password@testdb.xy.mongodb.net/DemoDB?retryWrites=true&w=majority")
        DB_URI = os.environ.get("DB_URI")
        print(DB_URI)

        self.REFRESH_RUN_COLLECTION = os.environ.get("REFRESH_RUN_COLLECTION", "refresh_run")


        self.USER_COLLECTION = os.environ.get("USER_COLLECTION", "user")

        self.USERS_CREDITENTALS_COLLECTION = os.environ.get("USERS_CREDITENTALS_COLLECTION", "usersCreditentals")


        r = os.environ.get("RETURN_AND_SAVE_DEFAULT_SETTINGS_IF_NO_RECORDS_FOUND", "False")
        self.RETURN_AND_SAVE_DEFAULT_SETTINGS_IF_NO_RECORDS_FOUND = True if r == "True" else False

        app.config["MONGODB_HOST"] = DB_URI

        self.db = MongoEngine(app)




config = Config()
