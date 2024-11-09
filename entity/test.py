import pickle

db = {'hi_score': 0, 
        'endless_play': 0, 
        'min_hp': 20,
        'story_play': 0, 
        'vic_count': 0}
with open('entity/data.pkl', 'wb') as file:
    pickle.dump(db, file)  

#reset db
