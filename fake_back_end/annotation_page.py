import urllib
import config
from database import DB, fetchMGDB
import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin
from __main__ import app


def find_entity(entity):
    q = 'SELECT rowid, * FROM entities WHERE context = ?;'
    d = DB.query(q, (entity, ))
    if len(d) == 0:
        return {}
    return {"text": d[0]['context'],
            "pos": [d[0]['startPos'], d[0]['endPos']], 
            "id": d[0]['rowid']}


def new_relation(doc_id, entity_1, entity_2):
    return {
        'relation_id': doc_id + ':' + 
        str(find_entity(entity_1)['id']) + '+' + str(find_entity(entity_2)['id']),
        'entity_1': entity_1,
        'entity_2': entity_2,
        'confirmed': 0,
        'score': 0,
        'relation': '?'}


@app.route('/annotation_page/<id>', methods = ['GET', 'POST'])
@cross_origin()
def annotate(id):
    # { "_id": ,
    #   "pmid": ,
    #   "entities": [{"text":, "pos": [0,1], "id"}],
    #   "text":
    #   "relations": [{"id", "h": {"text", "pos", "id"}, "t":, "relation", "score"}]
    # }
    if request.method == 'POST':
        confirmed_relations = request.json['confirmed']
        q = """INSERT INTO relations 
            (relation_id, entity_1, entity_2, relation, confirmed, score)
            VALUES (?, ?, ?, ?, 1, 1)
            ON CONFLICT (relation_id) DO
            UPDATE SET relation = ?, confirmed = 1;"""
        for relation_id, pair in confirmed_relations:
            p = (relation_id, pair['h'], pair['t'], pair['relation'], 
                pair['relation']) 
            DB.update(q, p)
        
        # q = """UPDATE relations SET relation = ?, confirmed = 1 
        #         WHERE relation_id == ?;"""
        # for i, r in confirmed_relations:
        #     DB.update(q, (r['relation'], i))
        return {"msg": True} 

    args = request.args
    entity_sel = list(set([args.get('entityA'), args.get('entityB')]) - set(['null']) - set([None]))
    # find document
    q = 'SELECT document_id, context, entity_fetched FROM documents WHERE document_id = ?;'
    doc = DB.query(q, (id, ))[0]
    document = {'_id': doc['document_id'], 'text': doc['context'], 'pmid': doc['document_id']}
    document_id = document['_id']

    if doc['entity_fetched'] == 0:
        print('fetching\n')
        entity_url = config.entity_extractor + '?document=' + urllib.parse.quote(document['text'], safe='')
        entities = requests.get(entity_url).json()
        # insert entities into db
        entity_fields = ['document_id', 'context', 'startPos', 'endPos', 'label']
        entity_rows = [(
            document_id, 
            e['entity'], 
            e['start'], 
            e['end'], 
            e['label']) for e in entities]
        DB.insert('entities', entity_fields, entity_rows)

        relation_url = config.triple_extractor + '?document=' + urllib.parse.quote(document['text'], safe='')
        relations = requests.get(relation_url).json()
        relations = list({(r[0], r[1]): r for r in relations}.values()) 

        # insert relations into db
        relation_fields = ['relation_id', 'entity_1', 'entity_2', 'relation', 'confirmed', 'score']
        relation_rows = [(document_id + ':' + str(find_entity(r[0])['id']) + '+' + str(find_entity(r[1])['id']), 
            r[0], r[1], r[2], 0, r[3]) for r in relations]
        DB.insert('relations', relation_fields, relation_rows)

        q = 'UPDATE documents SET entity_fetched = ? WHERE document_id = ?;'
        DB.update(q, (1, document_id))


    entity_q = 'SELECT rowid, context, startPos, endPos FROM entities WHERE document_id = ?;'
    entities = DB.query(entity_q, (document_id, ))
    entities = [{'text': e['context'], 'pos': [e['startPos'], e['endPos']], 'id': e['rowid']} for e in entities]

    # relation part
    relations = []
    print('entity_sel:', entity_sel)
    if len(entity_sel) == 0:
        data = {}
    elif len(entity_sel) == 1:
        entity = list(entity_sel)[0]
        q = """SELECT rowid, * FROM relations 
                WHERE (entity_1 == ? OR entity_2 == ?);"""
        data = {(d['entity_1'], d['entity_2']): d for d in DB.query(q, (entity, entity))}
        for ent in entities:
            e = ent['text']
            if e == entity:
                continue
            if (e, entity) not in data:
                data[(e, entity)] = new_relation(document_id, e, entity)
            if (entity, e) not in data:
                data[(entity, e)] = new_relation(document_id, entity, e)
        # data = [v for v in data.values() if v['confirmed'] == 0]
    else:
        entity_A, entity_B = list(entity_sel)
        q = """SELECT rowid, * FROM relations 
                WHERE ((entity_1 == ? AND entity_2 == ?) 
                        OR (entity_1 == ? AND entity_2 == ?));"""
        data = DB.query(q, (entity_A, entity_B, entity_B, entity_A))
        data = {(d['entity_1'], d['entity_2']): d for d in data}
        if (entity_A, entity_B) not in data:
            data[(entity_A, entity_B)] = new_relation(document_id, entity_A, entity_B)
        if (entity_B, entity_A) not in data:
            data[(entity_B, entity_A)] = new_relation(document_id, entity_B, entity_A)
    data = [v for v in data.values() if v['confirmed'] == 0]
    data = [{
        'id': d['relation_id'], 
        "h": find_entity(d['entity_1']), 
        "t": find_entity(d['entity_2']), 
        "relation": d['relation'], 
        "score": d['score']
        } for d in data]
    document.update({'relations': data, 'entities': entities})
    return document









