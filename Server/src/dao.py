from connection_manager import DB


def check_if_id_exists(table_name, id):
    query_string = 'Select * from ' + table_name + ' where id=%s'
    result_set = DB().query(query_string, [id,])
    if result_set.rowcount == 1:
        return True
    return False


def register_clienta(client_info):
    print('Registering clienta')
    client_id=client_info['site_id']
    address=client_info['address']
    description=client_info['description']
    contact=client_info['contact']
    nearest_node=client_info['nearest_node']
    is_prohibited=client_info['is_prohibited']
    q = 'INSERT INTO ClientA (ID,Description,Address,Contact,NearestNode,IsProhibited) values(%s,%s,%s,%s,%s,%s)'
    DB().query(q, (client_id, address, description, contact, nearest_node, is_prohibited))
    return None

def register_clientb(client_info):
    print('Registering clientb')
    client_id = client_info['site_id']
    address = client_info['address']
    description = client_info['description']
    contact = client_info['contact']
    q = 'INSERT INTO ClientB (ID,Description,Address,Contact) values(%s,%s,%s,%s)'
    DB().query(q, (client_id, address, description, contact))
    return None