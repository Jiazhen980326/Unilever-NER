# frontend for capstone

## fake backend

This backed code is developed for help developing frontend.  
download package  
```bash
git clone https://github.com/thunlp/OpenNRE.git
pip install -r requirements.txt
python setup.py install

pip3 install flask
pip3 install flask_cors
```
(first three lines are for opennre, refer to [this page](https://opennre-docs.readthedocs.io/en/latest/get_started/install.html))  
run the server:  
```bash
cd fake_back_end
python3 main.py
```
should see following  
```bash
xingyulu@Xingyus-MBP fake_back_end % python3 main.py
2022-10-07 07:00:53,667 - root - INFO - Initializing word embedding with word2vec.
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
2022-10-07 07:00:54,667 - werkzeug - INFO -  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
2022-10-07 07:00:54,668 - werkzeug - INFO -  * Restarting with stat
2022-10-07 07:01:03,135 - root - INFO - Initializing word embedding with word2vec.
2022-10-07 07:01:04,018 - werkzeug - WARNING -  * Debugger is active!
```
So the server runs on `http://127.0.0.1:5000/`  

## frontend
First check line 5 in `front_end/src/pages/input.js` and line 10 in `front_end/src/pages/annotate.js` if the input for useFetch is not server address + '/documents.....'; server address is what you get from previous part.  
Install the node.js and all react packages(netninja)  
Run the frontend
```bash
npm start
```


containarize
neo4j has python package 
insert into graph database triples


