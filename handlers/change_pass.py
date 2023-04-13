from main import app
from auth import login_required
from models import UsersCreditentals
from flask import jsonify, request
from config_loader import config
import hashlib
import uuid

@app.route("/changepass/email/<email>", methods=["GET",])
@login_required
def get_user_email(email:str):
    

      
        user_record = UsersCreditentals.objects(email=email.replace('\u200b',"")).first()
        
        if user_record:
           
            print(user_record.email)
            print(user_record.uuid)
            return jsonify(user_record.uuid)
        

        return "AAA"


@app.route("/changepass/auth/<auth>", methods=["GET",])
@login_required
def get_user_uuid(auth:str):
    

  
      
        user_record = UsersCreditentals.objects(uuid=auth).first()
        
        if user_record:
           
            print(user_record.email)
            print(user_record.uuid)
            return jsonify(user_record.uuid)
        

        return "AAA"


@app.route("/changepass/newpass/<email>", methods=["POST",])
@login_required
def post_user_pass(email:str):
    

  
        request_data = request.get_json()

        
        password = request_data['password']
      
        user_record = UsersCreditentals.objects(email=email).first()
        
         
        password = password.replace('\u200b',"").encode('utf-8')
        user_record.update(password=str(hashlib.md5(password).digest()))
        
        new_user = UsersCreditentals(
            userId=user_record.userId,
            password=str(hashlib.md5(password).digest()),
            email=email,
            uuid=user_record.uuid
        )
        if user_record:
           
            print(user_record.email)
            print(user_record.password)
            
            #UsersCreditentals.save(new_user)
            return jsonify(user_record.uuid)
        
    
        return "AAA"