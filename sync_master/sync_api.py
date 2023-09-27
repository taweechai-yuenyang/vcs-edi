import time
import pyodbc
import requests
import json

# Set your SQL Server connection parameter
server = 'localhost'
database = 'VCSDB'
username = 'sa'
password = 'ADSads123'


url = "http://localhost:8000/api/token/"

payload = 'username=taweechai&password=admin@vcs'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    obj = response.json()
    token = obj['access']
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=no;'
    # Establish a connection
    conn = pyodbc.connect(connection_string)
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
        
        payload = f'skid={FCSKID}&prod_type_id={FCTYPE}&code={FCCODE}&name={FCNAME}&description={FCNAME2}'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/product", headers=headers, data=payload)

        # print(response.text)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCSKID}")

    cursor.close()
    conn.close()
