import pickle
import os

file = "database.pkl"

def load(): #load data
    if os.path.exists(file): #check whether the pickle file is exist or not
        with open(file, "rb") as f:
            data = pickle.load(f)
            if "settings" not in data:
                data["settings"] = {"book_genid": 1} #set the book id start from 1
            if "paymentlog" not in data:
                data["paymentlog"] = []
            return data

    return { #return these data if no database found
        "books": {}, 
        "students": {}, 
        "settings": {"book_genid": 1},
        "paymentlog": []
    }

def save(data): #save data
    with open(file, "wb") as f:
        pickle.dump(data, f)



def bid_gen(data): #generate book id
    id = data['settings']['book_genid']
    while len(str(id)) < 7: #make sure it is 7 digits after B
        id = "0" + str(id)
    modified_id = "B" + str(id) #start with B
    
    data['settings']['book_genid'] = data['settings']['book_genid'] + 1 #generate a new book id and give them a new number
    return modified_id