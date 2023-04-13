from main import app
from auth import login_required
from models import UsersCreditentals
from flask import jsonify, request
from config_loader import config
import hashlib
import uuid

@app.route("/post/register/userCreditentals/", methods=["POST",])
@login_required
def post_user_registration():
    #user_record = UserCreditentals.objects(usrername=username).first()


        request_data = request.get_json()

        username = request_data['username'].replace('\u200b',"")
        password = request_data['password']
        password = password.replace('\u200b',"").encode('utf-8')
        email = request_data['email'].replace('\u200b',"")
        user_record = UsersCreditentals.objects(userId=username).first()
        user_record2 = UsersCreditentals.objects(email=email).first()
        
        new_user = UsersCreditentals(
            userId=username,
            password=str(hashlib.md5(password).digest()),
            email=email,
            uuid=str(uuid.uuid1())
        )
        #print(new_user.username)
        if(user_record or user_record2):
                
            if(username == user_record.userId and  email != user_record.email):
                  return "Postoji korisnik s istim korisničkim imenom, provjerite jeste li se već registrirali ili odaberite novo korisničko ime."
            else:
                  return "Postoji korisnik s istim korisničkim imenom, provjerite jeste li se već registrirali ili odaberite novo korisničko ime."
        else: 
            UsersCreditentals.save(new_user)
            user_record = new_user
            return "True"
    

    