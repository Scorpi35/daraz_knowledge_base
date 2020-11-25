import pickle
import requests
import json

url = "http://127.0.0.1:5000"

while (True):
    user_input = input("Ask a question:-")
    if (user_input == 'quit'):
        break
    data = {
        'question': user_input
    }
    response = requests.post(url, data)
    answer = json.loads(response.text)
    print("*************************************************")
    print("Category:-" + answer['category'])
    print("Answer:- " + answer["answer"])
    print("---------")
    print("Entities")
    print("---------")
    for entity in answer['entity_classification']:
        print(entity['raw_value'] + "----->" + entity['entity_type'])

    print("*************************************************")



