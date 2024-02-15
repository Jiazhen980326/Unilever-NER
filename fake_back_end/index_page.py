from database import DB
from flask import Flask, request
from flask_cors import CORS, cross_origin
from __main__ import app

@app.route("/index_page")
@cross_origin()
def read_documents():
    fields = ["rowid", "constr", "dbname", "collection", "idField", "docField", "fetched"]
    def find_info():
        q = "SELECT " + ','.join(fields[1:]) + " FROM input " \
                "WHERE rowid = ( SELECT max(rowid) FROM input )"
        data = DB.query(q, ())
        return data

    data = find_info()
    if len(data) == 0 or data[0]['fetched'] == 0:
    	return {"data": [{"_id": "000", "text": "DB not fetched yet", "pmid": "000"}]}

    q = "SELECT * from documents"
    docs = DB.query(q, ())
    docs = [{'_id': d['document_id'], 'text': d['context'], 'pmid': d['document_id']} for d in docs]
    # return {"say": "hello"}
    return {"data": docs}