import json


ar = []

with open('cenz.txt', encoding='utf-8') as cenz:
    for item in cenz:
        word = item.lower().split('\n')[0]
        if word != '':
            ar.append(word)

with open('cenz.json', 'w', encoding='utf-8') as cenz_dump:
    json.dump(ar, cenz_dump)
