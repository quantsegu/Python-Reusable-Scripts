#This code is written to extract code for SQL Stored Procedures , Functions and other objects from T-SQL
import pyodbc
import json
import pandas as pd

class ScriptDownloader:
    
    def __init__(self, folderName, connectionString):
        self.folderName = folderName
        self.connstring = connectionString
        
            
    def FetchObjectsAndStore(self, query):
        cnxn = pyodbc.connect(self.connstring, autocommit=True)
        df = pd.DataFrame()
        try:
            #cursor.execute(query)
            d = pd.read_sql_query(query, cnxn)
            df = pd.DataFrame(d)

            for i, r in df.iterrows():
                f = open(self.folderName + r[0] + '\\' + r[0] + "." + r[1] + '.sql', "w+")
                f.write(r[2])
                f.close()

        except pyodbc.Warning as warning:
            print(warning)

        finally:
            cnxn.close()
