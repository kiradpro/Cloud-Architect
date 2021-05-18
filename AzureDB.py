from datetime import datetime
import pypyodbc
import time
import math

import azurecred


class AzureDB:

    dsn='DRIVER='+azurecred.AZDBDRIVER+';SERVER='+azurecred.AZDBSERVER+';PORT=1433;DATABASE='+azurecred.AZDBNAME+';UID='+azurecred.AZDBUSER+';PWD='+ azurecred.AZDBPW


    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()


    def finalize(self):
        if self.conn:
            self.conn.close()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()


    def __enter__(self):
        return self


    def azureGetData(self):
        try:
            self.cursor.execute("SELECT * from data ORDER BY date DESC")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit (1)


    def azureGetDataid(self, id):
        try:
            self.cursor.execute("SELECT * from data WHERE id=?", (id,))
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit (1)


    def azureAddData(self, name, text):
        self.cursor.execute("INSERT INTO data (name, text) values (?, ?)", (name, text))
        self.conn.commit()

    
    def azureUpdateData(self, name, text, id):
        date = datetime.utcnow()
        self.cursor.execute("UPDATE data SET name=?, text=?, date=? WHERE id=?", (name,text,date,id))
        self.conn.commit()


    def azureDeleteData(self, id):
        self.cursor.execute("DELETE FROM data WHERE id=?", (id,))
        self.conn.commit()
