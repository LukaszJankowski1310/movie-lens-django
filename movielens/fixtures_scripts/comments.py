import os
import json
import datetime



data = None
with open("picked_comments.json", "r") as file:
    data = json.load(file)


comments_data = []

for id, comment in enumerate(data):


    text = comment['comment']
    author = int(comment['user'])
    date = int(comment['timestamp'])
    date = datetime.datetime.fromtimestamp(date)
    date = date.strftime('%Y-%m-%d')

    movie = int(comment['movie'])

    model = {
        "pk" : id+1,
        "model" : "userview.comment",
        "fields" : {
            'text' : text,
            'author' : author,
            'date' : date,
            'movie' : movie
        }
    }

    comments_data.append(model)



with open('data_comments.json', 'w') as file:
    json.dump(comments_data, file, indent=4) 