from database import DB, fetchMGDB
from flask import Flask, request
from flask_cors import CORS, cross_origin
from __main__ import app

@app.route('/new_entity', methods=['POST'])
@cross_origin()
def new_entity():
    data = request.json
    entity, doc_id = data['text'], data['doc_id']
    if len(DB.query(
        'SELECT rowid FROM entities WHERE document_id == ? AND context == ?', 
        (doc_id, entity))) == 0:
    	DB.insert('entities', ['document_id', 'context'], [(doc_id, entity)])
    return {"msg": True} 