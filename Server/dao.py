from connection_manger import DB


def check_if_id_exists(table_name, id):
    query_string = 'Select * from ' + table_name + ' where id=%s'
    result_set = DB().query(query_string, [id,])
    if result_set.rowcount == 1:
        return True
    return False