import os
import json
from django.contrib.auth.hashers import make_password 

import django
from django.conf import settings


settings.configure()

target_extension = ".json"
folder_path = "picked_users"


u = {
   "user_id": "1",
   "password": "llsna07%",
   "first_name": "Isla",
   "last_name": "Collins",
   "username": "isl49"
}

users_data = []

for filename in os.listdir(folder_path):
    if filename.find(target_extension) == -1:
        continue
    
    data = None
    with open(f'{folder_path}/{filename}') as file:
        data = json.load(file)
        pk = data['user_id']
        username = data['username']
        password = data['password']
        password = make_password(password)
        first_name = data['first_name']
        last_name = data['last_name']
      
    
    model = {
        'pk' : int(pk),
        'model' : 'auth.user',
        'fields' : {
            "username" : username,
            "password" : password,
            "first_name" : first_name,
            "last_name" : last_name,
            # "email" : ""
        }
    }

    users_data.append(model)

    # break

with open('data_users.json', 'w') as file:
    json.dump(users_data, file, indent=4)    