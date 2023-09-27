import pyodbc
import pymssql

conn = pymssql.connect(host=r'192.168.20.9:1433\Formula', user='fm1234', password='x2y2', charset='UTF-8', database=r'Formula', tds_version=r'7.0')

# # connection_string = str('Driver={ODBC Driver 18 for SQL Server};SERVER=192.168.20.9;DATABASE=Formula;UID=fm1234;PWD=x2y2;TrustServerCertificate=yes;')
# connection_string = str('DSN=EDIDB;UID=fm1234;PWD=x2y2;')
# # Establish a connection
# conn = pyodbc.connect(connection_string)
SQL_QUERY = f"""select FCSKID,FCTYPE,FCCODE,FCNAME,FCNAME2 from PROD"""
cursor = conn.cursor()
cursor.execute(SQL_QUERY)
i = 1
for r in cursor.fetchall():
    FCSKID = str(f"{r[0]}").strip()
    FCTYPE = f"{r[1]}".strip()
    FCCODE = str(f"{r[2]}").strip()
    FCNAME = str(f"{r[3]}").strip()
    FCNAME2 = str(f"{r[4]}").strip()
    
    payload = f'skid={FCSKID}&prod_type_id={FCTYPE}&code={FCCODE}&name={FCNAME}&description={FCNAME2}'
    print(payload)
cursor.close()
conn.close()