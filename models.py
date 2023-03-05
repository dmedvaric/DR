from mongoengine import EmbeddedDocument, StringField, EmbeddedDocumentListField, DynamicDocument, DateTimeField, \
    IntField
from config_loader import config


class Setting(EmbeddedDocument):
    settingDesc = StringField()
    settingName = StringField()
    settingValue = StringField()


class User(DynamicDocument):
    userId = StringField()
    lastUpdateTime = DateTimeField()
    settings = EmbeddedDocumentListField(Setting)

    meta = {'collection': config.USER_COLLECTION}

class UsersCreditentals(DynamicDocument):
    userId = StringField()
    password = StringField()
    email = StringField()
    uuid = StringField()

    meta = {'collection': config.USERS_CREDITENTALS_COLLECTION}



class RefreshRun(DynamicDocument):
    runTime = DateTimeField()
    updatedUserCount = IntField()

    meta = {'collection': config.REFRESH_RUN_COLLECTION}


class IncompleteXapiStatementError(Exception):
    pass
