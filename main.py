import handler
from flask import Flask,render_template,redirect,request,abort,make_response
from pymongo import MongoClient
import datetime
myclient =MongoClient("mongodb://localhost:27017/")
db = myclient["iplogger"]


app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<destination>')
def redirect_to_desired_url(destination):
    url=db.urls.find_one({"code":destination})
    if url:
        db.logs.insert_one({"code":destination,"ip":request.remote_addr,"time":datetime.datetime.now()})
        return redirect(f"http://{url['url']}")
    else:
        abort(400)

@app.route('/api/create')
def create():
    url=request.args['url']
    url_code=handler.generate_url_string(5)
    db.urls.insert_one({"code":url_code,"url":url})
    return f"<pre>{request.url_root}{url_code}  \nTrack Here: {request.url_root}track/{url_code}</pre>"

@app.route('/track/<destination>')
def send_logs(destination):
    records=db.logs.find({"code":destination})
    item_list=[]
    for items in records:
        item_list.append(items)
    return render_template('track.html',logs=item_list)


app.run(debug=False,port=5001)