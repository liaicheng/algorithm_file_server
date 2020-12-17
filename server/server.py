import json
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import redis
import hashlib
from os.path import dirname,abspath
from util import date
import workflow_manager

DATA_ROOT = "/Users/lac/PycharmProjects/algorithm_file_server/data/"
HTOKEN= hashlib.md5()

REDIS_CLI = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

WM = workflow_manager.WorkflowManager(REDIS_CLI)

root = dirname(dirname(abspath(__file__)))
app = Flask("adp", static_folder = root + "/data/",static_url_path="/data")



@app.route('/token', methods=['POST'])
def get_token():
    data = request.get_json()
    name = data.get("name","")
    pwd = data.get("password","")
    print(name,pwd)
    pwd_rd = REDIS_CLI.get(name)
    print(name, str(pwd),pwd_rd.decode("utf-8"))
    if str(pwd) == str(pwd_rd.decode("utf-8")):
        date_str = date.get_date_str()
        print(name+"_"+date_str)
        HTOKEN.update((name+"_"+date_str).encode('utf-8'))
        token = HTOKEN.hexdigest()
        REDIS_CLI.set(token,0)
        REDIS_CLI.expire(token,3600*30)
        return {"data":{"token":token},"message":"Success"}, 200
    else:
        return {"data":{"token":""},"message":"Not Auth"},401


@app.route('/file_list/', methods=['GET'])
def get_file_list():
    token = request.args.get("token")
    if REDIS_CLI.get(token) is None:
        return {"data":{},"message":"Wrong Token"}, 404

    keys = REDIS_CLI.keys("u00*")
    values = REDIS_CLI.mget(keys)
    res = []
    for k,v in enumerate(values):
        if v == b"preprocess":
            res.append(keys[k])
    return {"data":{"file":res},"message":"Success"}, 200


@app.route('/upload/<name>', methods=['POST'])
def upload_file(name):
    print(request)
    token = request.args.get("token")
    if REDIS_CLI.get(token) is None:
        return {"data": {}, "message": "Wrong Token"}, 404

    f = request.files['file']
    upload_path = os.path.join(DATA_ROOT,'result/uploads', name)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)
    WM.on_finish(name)
    return {"data":{},"message":"Success"}, 200

@app.route('/download/<name>', methods=['POST'])
def download_file(name):
    token = request.args.get("token")
    print("ttt",token)
    if REDIS_CLI.get(token) is None:
        return {"data": {}, "message": "Wrong Token"}, 404
    res = WM.on_process(name)
    if res == "":
        return {"data":{},"message":"Not Found"}, 404
    print("rrrrr",res)
    return {"data":{"file":res},"message":"Success"}, 200

# UPLOAD_FOLDER = '/Users/lac/PycharmProjects/algorithm_file_server'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_files():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             print(filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return ""
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001, debug=True)