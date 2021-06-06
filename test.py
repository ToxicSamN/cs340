from animal_shelter import AnimalShelter
import os

dbo = AnimalShelter("aacuser", "password", "localhost", 52170, "AAC")

try:
    new_doc = {
        '1': 9999,
        'age_upon_outcome': '2 months',
        'animal_id': 'SammyTest',
        'animal_type': 'Dog',
        'breed': 'Newfoundland/Australian Cattle Dog',
        'color': 'Black/White',
        'date_of_birth': '2013-08-16',
        'datetime': '2013-10-20 17:46:00',
        'monthyear': '2013-10-20T17:46:00',
        'name': 'Flynn', 'outcome_subtype': '',
        'outcome_type': 'Adoption',
        'sex_upon_outcome': 'Neutered Male',
        'location_lat': 30.3822258965608,
        'location_long': -97.3215567924164,
        'age_upon_outcome_in_weeks': 9.39146825396825
    }
    result = dbo.create(new_doc)
    if result:
        for doc in dbo.read({"animal_id": "SammyTest"}):
            print(doc)
        print("document creation was successful")

    else:
        print("test failed creating 1 new doc")

except BaseException as e:
    print(f'suppressing CREATE exceptions right now\n{e}')

try:
    for doc in dbo.read({"animal_id": "SammyTest"}):
        print(doc)
        print("document read success")
except NotImplementedError as e:
    print(f'suppressing READ exceptions right now\n{e}')

try:
   dbo.update({"animal_id": "SammyTest"}, {"$set": {"animal_id": "NewSammyTest"}})
   for doc in dbo.read({"animal_id": "NewSammyTest"}):
       print(doc)
       print("document update success")

except NotImplementedError as e:
   print(f'suppressing UPDATE exceptions right now\n{e}')

try:
    if dbo.delete({"animal_id": "NewSammyTest"}):
        print("delete record success")
    else:
        print("delete record failed")
except NotImplementedError as e:
    print(f'suppressing DELETE exceptions right now\n{e}')
