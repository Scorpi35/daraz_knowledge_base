from __future__ import unicode_literals, print_function
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import pickle
from flask import Flask, render_template, json, request
import json
import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN


with io.open("Knowledge_Base/Entitiy_Category/Questions_Entity.json") as f:
    entity_category_dataset = json.load(f)

nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
nlu_engine = nlu_engine.fit(entity_category_dataset)

app = Flask(__name__)
DarazBot = ChatBot(name='BankBot',
                   read_only=False,
                   logic_adapters=["chatterbot.logic.BestMatch"],
                   storage_adapter="chatterbot.storage.SQLStorageAdapter")

# Building custom knowledge base

training_list = ["campaign.pkl",
  "daraz_mall.pkl",
  "my_account.pkl",
  "ordering.pkl",
  "payments.pkl",
  "return_refund.pkl",
  "shopping_delivery.pkl",
  "voucher_promotions.pkl"]


# Knowledge base for my account


trainer = ListTrainer(DarazBot)

for training_file in training_list:
    path = "Knowledge_Base/Question_Answers/" + training_file
    with open(path, 'rb') as f:
        trainer.train(pickle.load(f))


#define app routes
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        user_question = request.form['question']
        answer = DarazBot.get_response(user_question)
        entitiy_category = nlu_engine.parse(user_question)
        category = entitiy_category["intent"]["intentName"]
        entities = []
        for entity in entitiy_category['slots']:
            item = {
                'entity_type': entity['entity'],
                'raw_value': entity['rawValue']
            }

            entities.append(item)

        response = {
            "answer": str(answer),
            "category": category,
            "entity_classification": entities
        }
        response = json.dumps(response)
        return response
    else:
        return "Ask Question"


if __name__ == "__main__":
    app.run()
