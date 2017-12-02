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
if __name__=='__main__':
    app.run(host='0.0.0.0',port=7777,debug=True)