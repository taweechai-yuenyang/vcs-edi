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
    conn = pymssql.connect(host=r'192.168.20.9:1433\Formula', user='fm1234', password='x2y2', charset='TIS-620', database=r'Formula', tds_version=r'7.0')
    
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
        FCSKID = str(f"{r[0]}").strip()
        FCCODE = str(f"{r[1]}").strip()
        FCNAME = str(f"{r[2]}").strip()
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
        FCCODE = str(f"{r[0]}").strip()
        FCNAME = str(f"{r[1]}").strip()
        FCNAME2 = str(f"{r[2]}").strip()
        
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
        time.sleep(0.1)
    
    SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from UM"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCCODE = str(f"{r[0]}").strip()
        FCNAME = str(f"{r[1]}").strip()
        FCNAME2 = str(f"{r[0]}").strip() + '-' + str(f"{r[1]}").strip()
        
        payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}'.encode('utf8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'}

        response = requests.request(
            "POST", "http://localhost:8000/api/unit", headers=headers, data=payload)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
        i += 1
        time.sleep(0.1)
    
    SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from REFTYPE"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCCODE = str(f"{r[0]}").strip()
        FCNAME = str(f"{r[1]}").strip()
        FCNAME2 = str(f"{r[2]}").strip()
        
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
        time.sleep(0.1)
        
    SQL_QUERY = f"""select FCSKID,FCTYPE,FCCODE,FCNAME,FCNAME2 from PROD"""
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    err = []
    i = 1
    for r in cursor.fetchall():
        FCSKID = str(f"{r[0]}").strip()
        FCTYPE = str(f"{r[1]}").strip()
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
        if response.status_code != 201:
            err.append(FCCODE)
            
        print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
        i += 1
        time.sleep(0.1)

    cursor.close()
    conn.close()
    print(err)