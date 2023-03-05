from main import app
from auth import login_required
from models import UsersCreditentals
from flask import jsonify, request
from config_loader import config
import hashlib
import uuid

@app.route("/analiticarka/get/login/<username>", methods=["POST",])
@login_required
def post_user_login(username:str):
    

   #if user_record:
        #user_record = user_record
        #return "korisnicko ime postoji s drugim mailom"
        request_data = request.get_json()
        username = request_data['username'].replace('\u200b',"")
        checkPass = request_data['password'].replace('\u200b',"").encode('utf-8')
        user_record = UsersCreditentals.objects(userId=username).first()
        
        if user_record:
            print("USAO?")
            user_record = user_record
            print(user_record.password)
            checkPassHash = str(hashlib.md5(checkPass).digest())
            print(checkPassHash)
            print(jsonify(user_record))
            if(checkPassHash == user_record.password):
                  print("ovo?")
                  return "True"
                  
            else:
                  print("ovo nestovno?")
                  return "False"
            #return jsonify(user_record)
        
      #  password = request_data['password'].encode('utf-8')
        

       # print(user_record.json())

     #   UsersCreditentals.save(new_user)
        #user_record = new_user
        return "AAA"