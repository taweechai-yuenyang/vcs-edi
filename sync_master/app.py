import pymssql
import time
import requests
import json

urlAPI = "http://localhost:8000"
objHeader = {'Content-Type': 'application/x-www-form-urlencoded',}
userLogIn = 'username=taweechai&password=ADSads123'

dbHost = '192.168.20.9:1433'
dbUser = 'fm1234'
dbPassword = 'x2y2'
dbName = 'Formula'
dbCharset = 'TIS-620'


def sync_supplier():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCSKID,FCCODE,FCNAME from COOR c WHERE FCISSUPP='Y' order by c.FCCODE,c.FCNAME"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCSKID = str(f"{r[0]}").strip()
            FCCODE = str(f"{r[1]}").strip()
            FCNAME = str(f"{r[2]}").strip()
            payload = f'code={FCCODE}&name={FCNAME}&description=-&is_active=1'.encode(
                'utf8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'}

            response = requests.request(
                "POST", f"{urlAPI}/api/supplier", headers=headers, data=payload)

            # print(response.text)
            if response.status_code != 201:
                err.append(FCSKID)

            print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCSKID}")
            i += 1
            # time.sleep(0.1)
            
        cursor.close()
        conn.close()
        print(f"============== Supplier =================")
        print(err)
        print(f"=========================================")

def sync_product_type():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from PRODTYPE"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCCODE = str(f"{r[0]}").strip()
            FCNAME = str(f"{r[1]}").strip()
            FCNAME2 = str(f"{r[2]}").strip()

            payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}&is_active=1'.encode(
                'utf8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'}

            response = requests.request(
                "POST", f"{urlAPI}/api/product_type", headers=headers, data=payload)

            # print(response.text)
            if response.status_code != 201:
                err.append(FCCODE)

            print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
            i += 1
            # time.sleep(0.1)
            
        cursor.close()
        conn.close()
        print(f"============== Product Type =============")
        print(err)
        print(f"=========================================")


def sync_um():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from UM"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCCODE = str(f"{r[0]}").strip()
            FCNAME = str(f"{r[1]}").strip()
            FCNAME2 = str(f"{r[0]}").strip() + '-' + str(f"{r[1]}").strip()

            payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}&is_active=1'.encode(
                'utf8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'}

            response = requests.request(
                "POST", f"{urlAPI}/api/unit", headers=headers, data=payload)

            print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
            i += 1
            # time.sleep(0.1)
            
        cursor.close()
        conn.close()
        print(f"============== Unit Type =============")
        print(err)
        print(f"======================================")


def sync_order_type():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from REFTYPE"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCCODE = str(f"{r[0]}").strip()
            FCNAME = str(f"{r[1]}").strip()
            FCNAME2 = str(f"{r[2]}").strip()

            payload = f'code={FCCODE}&name={FCNAME}&description={FCNAME2}&is_active=1'.encode(
                'utf8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'}

            response = requests.request(
                "POST", f"{urlAPI}/api/order_type", headers=headers, data=payload)

            # print(response.text)
            if response.status_code != 201:
                err.append(FCCODE)

            print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
            i += 1
            # time.sleep(0.1)
            
        cursor.close()
        conn.close()
        print(f"============== Order Type =============")
        print(err)
        print(f"=======================================")


def sync_product():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCSKID,FCTYPE,FCCODE,FCNAME,FCNAME2 from PROD order by FCCODE,FCNAME"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCTYPE = str(f"{r[1]}").strip()
            FCCODE = str(f"{r[2]}").strip()
            FCNAME = str(f"{r[3]}").strip()
            FCNAME2 = str(f"{r[4]}").strip()
            if len(FCNAME2) == 0:
                FCNAME2 = f"{FCCODE}-{FCNAME}"

            payload = f'prod_type_id={FCTYPE}&code={FCCODE}&name={FCNAME}&description={FCNAME2}&is_active=1'.encode(
                'utf8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'}

            response = requests.request(
                "POST", f"{urlAPI}/api/product", headers=headers, data=payload)

            # print(response.text)
            if response.status_code != 201:
                if response.status_code == 401:
                    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
                    obj = response.json()
                    token = obj['access']
                
                elif response.status_code == 400:
                    print(response.text)
                    
                err.append(FCCODE)
                
            print(f"{i}.Sync PROD Status Code:{response.status_code} DataID: {FCCODE}")
            i += 1
            
        cursor.close()
        conn.close()
        print(f"============== Product =============")
        print(err)
        print(f"====================================")


if __name__ == "__main__":
    # sync_supplier()
    # sync_product_type()
    # sync_um()
    # sync_order_type()
    sync_product()
