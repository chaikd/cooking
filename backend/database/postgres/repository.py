from database.postgres.postgres import database


class RepositoryManager:
    def __init__(self):
        pass

    def insert(self, table_name, *info):
       def insert_cb(connection):
           # connection.query(f'''
           #  INSERT TO {table_name}
           #
           # ''')
            pass

       database.action(insert_cb)

