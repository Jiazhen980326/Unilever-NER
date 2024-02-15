from database import DB, fetchMGDB
from flask import Flask, request
from flask_cors import CORS, cross_origin
from __main__ import app

@app.route('/input_page', methods=['GET', 'POST'])
@cross_origin()
def input_page():
    fields = ["rowid", "constr", "dbname", "collection", "idField", "docField"]
    def find_info():
        query = "SELECT " + ','.join(fields[1:]) + " FROM input " \
                "WHERE rowid = ( SELECT max(rowid) FROM input )"
        params = ()
        data = DB.query(query, params)
        return data

    def check_update(prev, curr):
        for k in fields[1:]:
            if prev[k] != curr[k]:
                return True
        return False

    if request.method == 'POST':
        # check whether need update 
        prevData = find_info()
        reqj = request.json
        if len(prevData) == 0 or check_update(prevData[0], reqj):
            table = 'input'
            data = [[k, v] for k, v in reqj.items()] + [['fetched', 0]]
            DB.insert(table, [d[0] for d in data], [tuple([d[1] for d in data])])
            # fetch data from mongoDB
            fetchMGDB(*[reqj[k] for k in fields[1:]])

        return {"msg": True}

    data = find_info()
    if len(data) == 0:
        return {k: "null" for k in fields[1:]}
    else:
        return data[0]