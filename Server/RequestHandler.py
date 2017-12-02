from flask import Flask,jsonify,request,send_file
import dao
app=Flask(__name__)

@app.route('/',methods=['GET'])
def hand_shake():
    return jsonify(True)
@app.route('/register_clientA',methods=['POST'])
def register_clientA():
    response_dict=request.get_json()

@app.route('/check_id_exists',methods=['POST'])
def check_id_exists():
    response_dict=request.get_json()
    client_type=response_dict["clientType"]
    id=response_dict["id"]
    return jsonify(dao.check_if_id_exists(cliebt_type,id))
if __name__=='__main__':
    app.run(host='0.0.0.0',port=7777,debug=True)