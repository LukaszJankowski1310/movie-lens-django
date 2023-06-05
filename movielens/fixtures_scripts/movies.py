import os
import json

# result_file = open("data.json", "a")

target_extension = ".json"
folder_path = "picked_movies"

genres = []
movies_data = []
imgs_data = []

images_counter_id = 1

for filename in os.listdir(folder_path):
    if filename.find(target_extension) == -1:
        continue
    
    with open(f'{folder_path}/{filename}') as file:
        data = json.load(file)

    g = str(data['genre']).split(",")
    for gen in g:
        genres.append(gen.strip())

genres = list(set(genres))    
print(genres)
print(len(genres))

for filename in os.listdir(folder_path):
    if filename.find(target_extension) == -1:
        continue

    with open(f'{folder_path}/{filename}') as file:
        data = json.load(file)

    pk = int(filename.split(".")[0])
    model = 'userview.movie'
    title = data['title']
    genre = data['genre']
    imdbLink = data['imdbLink']

    data_movie = {
        'model' : model,
        'pk' : pk,
        'fields' : {
            'title' : title,
            'genres' : [genres.index(gen.strip())+1 for gen in genre.split(",")],
            'imdb_ref' : imdbLink
        }

    }

    movies_data.append(data_movie)



    image = data['image']
    
    data_img = {
        'model' : 'userview.image',
        'pk' : images_counter_id,
        'fields' : {
            'path' : image,
            'isFrontImage' : True,
            'movie' : pk 
        }
    }

    images_counter_id+=1
    imgs_data.append(data_img)





   
       
l = []     

for id, genre in enumerate(genres):
    data = {
        "pk" : id+1,
        "model" : "userview.genre",
        "fields": {
            'name': genre
        }
    }   
       
    l.append(data) 
       

with open('data_genres.json', 'w') as file:
    json.dump(l, file, indent=4)     
      

with open('data_movies.json', 'w') as file:
    json.dump(movies_data, file, indent=4)         
       
       
       
with open('data_images.json', 'w') as file:
    json.dump(imgs_data, file, indent=4)         
       

## comments





# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     if os.path.isfile(file_path) and filename.endswith(target_extension):
#         # Perform operations on files with the target extension
#         print(file_path)