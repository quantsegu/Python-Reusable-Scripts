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
            
#
#  ------------------------------------------- Stored Procedures  ---------------------------------------------
# SELECT  s.name SchemaName
#       ,o.name FunctionName
#       ,  sm.definition  
# FROM sys.sql_modules AS sm 
# JOIN sys.objects AS o 
# ON sm.object_id = o.object_id  
# left join sys.schemas s 
# on s.schema_id = o.schema_id
# WHERE o.name like 'usp%'
# ------------------------------------------- Functions---------------------------------------------------------
# y = x.FetchObjectsAndStore('''SELECT  s.name SchemaName
#       ,o.name FunctionName
#       ,  sm.definition  
# FROM sys.sql_modules AS sm 
# JOIN sys.objects AS o 
# ON sm.object_id = o.object_id  
# left join sys.schemas s 
# on s.schema_id = o.schema_id
# WHERE o.name like \'uf%\''''
# ------------------------------------------- Views---------------------------------------------------------
#y = x.FetchObjectsAndStore("select s.name as SchemaName,v.name as ViewName,definition from sys.objects     o join sys.sql_modules m on m.object_id = o.object_id join sys.views v on o.object_id = v.object_id join sys.schemas s on v.schema_id = s.schema_id where o.type      = 'V' and s.name = 'dbo' order by 1")
