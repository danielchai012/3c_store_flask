import pyodbc

server = '192.168.62.47'
database = 'pos'
username = 'itm'
password = 'itm123'
port = '3306'
driver = 'MySQL ODBC 8.0 Unicode Driver'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+database+'; UID='+username+'; PWD='+ password+';OPTION=3;CHARSET=UTF8;')