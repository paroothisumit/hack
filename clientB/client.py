import json
import os,requests,sys
from pathlib import  Path

def does_id_exist(site_id,node_type):
    response = requests.post(server_address + 'check_id_exists', json={'node_type': node_type, 'site_id': site_id})
    return response.json()

def is_server_address_correct():
    try:
        response = requests.get(server_address)
        print(response.status_code)
        return response.status_code == 200
    except Exception:
        return False


if is_server_address_correct():
    print('Server Responded')


def register_client():
    response = requests.post(server_address + 'register_clientb', json=json.dumps(configuration))
    return response.json()

def initialize():
    global configuration
    cwd = os.getcwd()
    conf_file_name = 'conf.txt'

    conf_file_path = Path(cwd + '/' + conf_file_name)
    if conf_file_path.is_file():
        print('configuration file found')

        with open(conf_file_name) as infile:
            configuration = (json.load(infile))
        if not does_id_exist(configuration["site_id"], 'clientb'):
            print('Corrupt Configuration File; Delete configuration file and restart')
            sys.exit(0)

    else:
        print('Setting up....ClientB')
        while True:
            id = input('Enter SiteID')
            if not does_id_exist(id, 'clientb'):
                break;
            print('This id already exists')

        address = input('Enter address')
        description = input('Enter description')
        contact = input('Enter contact')


        configuration = {"site_id": id, "address": address, "description": description, "contact": contact,
                        }
        with open(conf_file_name, 'w') as outfile:
            json.dump(configuration, outfile)
        register_client()





server_address=input('Enter server address:port')

server_address='http://'+server_address+'/'
configuration=None
initialize()



