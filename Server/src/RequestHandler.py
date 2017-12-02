import os

import errno
from pathlib import Path

from flask import Flask,jsonify,request,send_file,json
import dao
app=Flask(__name__)

@app.route('/',methods=['GET'])
def hand_shake():
    return jsonify(True)

@app.route('/register_clientb', methods=['POST'])
def register_clientb():

    request_dict = json.loads(request.get_json())
    print(type(request_dict))

    dao.register_clientb(request_dict)

    return jsonify(True)

@app.route('/fetch_settings', methods=['POST'])
def fetch_settings():
    request_dict=request.get_json()
    config_settings=dao.fetch_settings(request_dict["site_id"])
    return jsonify(config_settings)

@app.route('/register_clienta',methods=['POST'])
def register_clienta():
    request_dict=json.loads(request.get_json())
    dao.register_clienta(request_dict)
    return jsonify(True)

@app.route('/check_id_exists',methods=['POST'])
def check_id_exists():
    response_dict=request.get_json()
    print(response_dict)
    client_type=response_dict['node_type']
    id=response_dict['site_id']
    return jsonify(dao.check_if_id_exists(client_type,id))


@app.route('/new_alert', methods=['POST'])
def new_alert():
    print(request.get_json())
    request_dict = json.loads(request.get_json())
    dao.store_new_alert(request_dict["site_id"], request_dict["activity_recognized"], request_dict["cctv_location"],request_dict["time"])

    return jsonify(True)

@app.route('/check_new_alert', methods=['POST'])
def check_new_alert():
    print(request.get_json())
    request_dict=request.get_json()
    new_alerts=dao.check_new_alerts(request_dict["site_id"], request_dict["last_checked"])

    return jsonify(new_alerts)


def create_upload_folder():
    upload_folder_name = 'uploads'
    upload_folder_path = Path(os.getcwd() + '/' + upload_folder_name)
    try:
        os.makedirs(upload_folder_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__=='__main__':
    create_upload_folder()
    app.run(host='0.0.0.0',port=7777,debug=True)