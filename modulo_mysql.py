
#!/bin/python3

import mysql.connector






class UseDatabase:

    def __init__(self, config: dict):
        self.configuracao = config
    
    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuracao)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


