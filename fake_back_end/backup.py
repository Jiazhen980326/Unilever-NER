import os.path
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin


# models
import spacy
from spacy import displacy
import re
import opennre

from database import DB


NRE = opennre.get_model('wiki80_cnn_softmax')
NER = spacy.load("en_core_web_sm")



def get_entities(s):
    text = NER(s)
    entities = []
    for e in text.ents:
        length = len(str(e))
        lefts = [m.start() for m in re.finditer(str(e), s)]
        entities += [{"text": str(e), "pos": [l, l+length]} for l in lefts]
    for i in range(len(entities)):
        entities[i]['id'] = i
    # TODO: need a better way to define the entity id
    return entities


def infer_relations(s, h, t):
    relation, score = NRE.infer({'text': s, 'h': {'pos': h['pos']}, 't': {'pos': t['pos']}})
    # return {'h': h, 't': entities[j], 'relation': relation, 'score': score}
    return (relation, score)

def get_relation(s, h, t, relations):
    # first check existance, if not exist, calc
    if h['id'] not in relations:
        relations[h['id']] = {'info': h}
    if t['id'] not in relations[h['id']]:
        relations[h['id']][t['id']] = {'info': t}
        relations[h['id']][t['id']]['r'] = infer_relations(s, h, t)
    return {
        'id': str(h['id']) + '-' + str(t['id']),
        'h': h, 
        't': t, 
        'relation': relations[h['id']][t['id']]['r'][0],
        'score': relations[h['id']][t['id']]['r'][1]
    }

# flask backend
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if not os.path.exists('docs'):
    os.mkdir('docs')

@app.route("/")
@cross_origin()
def read_root():
    return {"say": "hello"}

@app.route("/index_page")
@cross_origin()
def read_documents():
    # {"data": [{"_id", "text", "pmid"}]}

    with open('data.json', 'r') as f:
        data = json.load(f)
    # return {"say": "hello"}
    return {"data": data}

@app.route('/input_page', methods=['GET', 'POST'])
@cross_origin()
def input_page():
    if request.method == 'POST':
        print('haha\n\n', request.json)
        return {"msg": True}

    return {"msg": False}


@app.route('/annotation_page/<id>', methods = ['GET', 'POST'])
@cross_origin()
def annotate(id):
    # { "_id": ,
    #   "pmid": ,
    #   "entities": [{"text":, "pos": [0,1], "id"}],
    #   "text":
    #   "relations": [{"id", "h": {"text", "pos", "id"}, "t":, "relation", "score"}]
    # }
    # if parameter entityA and entityB all null or not exist: relations = []
    # if one exist, relations = all pairs that has the parameter as text of h or text of t.
    # if both exist, relations = only pairs from one text to another.
    # note in the second and third case, one kind of parameter can have multiple positions
    
    # relations satisfy the condition: if t,
    if request.method == 'POST':
        print('haha\n\n', request.json['confirmed'])
        return {"msg": True}
    args = request.args
    entity_sel = [args.get('entityA'), args.get('entityB')]
    if entity_sel[0] == 'null':
        entity_sel[0] = None
    if entity_sel[1] == 'null':
        entity_sel[1] = None
    print(entity_sel)
    path = 'docs/'+id+'.json'
    print(entity_sel)
    # load data
    if not os.path.exists(path):
        with open('data.json', 'r') as f:
            data = json.load(f)
        data = [d for d in data if d['_id'] == id][0]
        entities = get_entities(data["text"])
        data.update({
                "entities": entities, 
                "relations": {}
            })
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=4))
    else:
        with open(path, 'r') as f:
            data = json.load(f)
    # lazy load the relations
    cand_ents = [
        [e for e in data['entities'] if e['text'] == entity_sel[0]], 
        [e for e in data['entities'] if e['text'] == entity_sel[1]]
    ]
    rels = []
    if entity_sel[0] and entity_sel[1]:
        for h in cand_ents[0]:
            for t in cand_ents[1]:
                rels.append(get_relation(data['text'], h, t, data['relations']))
                rels.append(get_relation(data['text'], t, h, data['relations']))
    elif entity_sel[0]:
        for h in cand_ents[0]:
            for t in data["entities"]:
                if t['text'] != h['text']:
                    rels.append(get_relation(data['text'], h, t, data['relations']))
                    rels.append(get_relation(data['text'], t, h, data['relations']))
    elif entity_sel[1]:
        for h in cand_ents[1]:
            for t in data["entities"]:
                if t['text'] != h['text']:
                    rels.append(get_relation(data['text'], h, t, data['relations']))
                    rels.append(get_relation(data['text'], t, h, data['relations']))
    if len(rels) != 0:
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=4))
    data['relations'] = rels
    print(len(rels), len(cand_ents[0]), len(cand_ents[1]))
    with open('obs.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
    return data

if __name__ == '__main__':
    app.run(debug=True)

# mongodb
# CONNECTION_STRING = "???"
# name, collection = '???', '???'

# def get_collection(name, collection):
#    client = MongoClient(CONNECTION_STRING)
#    return client[name][collection]

# collection = get_collection(name, collection)
# item_details = collection.find()

# for item in item_details:
#   ...

