import os
import json


data = None
with open("picked_ratings.json", "r") as file:
    data = json.load(file)
# {
#       "user_id": "1",
#       "movie_id": "1",
#       "rating": "4.0"
#    }

ratings_data = []

for id, rating in enumerate(data):
    value = rating['rating']
    user = rating['user_id']
    movie = rating['movie_id']

    model = {
        "pk" : id+1,
        "model" : "userview.rating",
        "fields" : {
            'value' : int(float(value)),
            'movie' : int(movie),
            'user' : int(user)
        }
    }

    ratings_data.append(model)



with open('data_ratings.json', 'w') as file:
    json.dump(ratings_data, file, indent=4) 