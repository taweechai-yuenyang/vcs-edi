import pymssql
import time
import requests
import json

url = "http://localhost:8000/api/token/"

payload = 'username=taweechai&password=ADSads123'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    obj = response.json()
    token = obj['access']
    conn = pymssql.connect(
        server='192.168.20.9',
        user='fm1234',
        password='x2y2',
        database='Formula',
        as_dict=True,
        charset='TIS-620'
    )
    
    # conn = pymssql.connect(
    #     server='localhost',
    #     user='sa',
    #     password='ADSads123',
    #     database='',
    #     as_dict=True,
    #     charset='TIS-620'
    # )

    SQL_QUERY = f"""select FCSKID,FCCODE,FCNAME from COOR c WHERE FCISSUPP='Y' order by c.FCCODE,c.FCNAME"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCSKID = str(f"{r['FCSKID']}").strip()
        FCCODE = str(f"{r['FCCODE']}").strip()
        FCNAME = str(f"{r['FCNAME']}").strip()
        payload = f'skid={FCSKID}&code={FCCODE}&name={FCNAME}&description=-'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/supplier", headers=headers, data=payload)

        # print(response.text)
        if response.status_code != 201:
            err.append(FCSKID)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCSKID}")
        i += 1
        
    SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from PRODTYPE"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCCODE = str(f"{r['FCCODE']}").strip()
        FCNAME = str(f"{r['FCNAME']}").strip()
        FCNAME2 = str(f"{r['FCNAME2']}").strip()
        
        payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/product_type", headers=headers, data=payload)

        # print(response.text)
        if response.status_code != 201:
            err.append(FCCODE)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
        i += 1
    
    SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from UM"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCCODE = str(f"{r['FCCODE']}").strip()
        FCNAME = str(f"{r['FCNAME']}").strip()
        FCNAME2 = str(f"{r['FCCODE']}").strip() + '-' + str(f"{r['FCNAME']}").strip()
        
        payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/unit", headers=headers, data=payload)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
        i += 1
    
    SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from REFTYPE"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCCODE = str(f"{r['FCCODE']}").strip()
        FCNAME = str(f"{r['FCNAME']}").strip()
        FCNAME2 = str(f"{r['FCNAME2']}").strip()
        
        payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/order_type", headers=headers, data=payload)

        # print(response.text)
        if response.status_code != 201:
            err.append(FCCODE)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
        i += 1
        
    SQL_QUERY = f"""select FCSKID,FCTYPE,FCCODE,FCNAME,FCNAME2 from PROD"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCSKID = str(f"{r['FCSKID']}").strip()
        FCTYPE = str(f"{r['FCTYPE']}").strip()
        FCCODE = str(f"{r['FCCODE']}").strip()
        FCNAME = str(f"{r['FCNAME']}").strip()
        FCNAME2 = str(f"{r['FCNAME2']}").strip()
        
        payload = f'skid={FCSKID}&prod_type_id={FCTYPE}&code={FCCODE}&name={FCNAME}&description={FCNAME2}'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/product", headers=headers, data=payload)

        # print(response.text)
        if response.status_code != 201:
            err.append(FCCODE)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
        i += 1

    cursor.close()
    conn.close()
    print(err)