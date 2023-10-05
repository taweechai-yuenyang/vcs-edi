import pymssql
import time
import requests
import json

urlAPI = "http://localhost:8000"
objHeader = {'Content-Type': 'application/x-www-form-urlencoded',}
userLogIn = 'username=taweechai&password=ADSads123'

# dbHost = '192.168.20.9:1433'
# dbUser = 'fm1234'
# dbPassword = 'x2y2'
# dbName = 'Formula'
# dbCharset = 'TIS-620'
dbHost = 'localhost:1433'
dbUser = 'sa'
dbPassword = 'ADSads123'
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
        
def sync_employee():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from EMPL"""
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
                "POST", f"{urlAPI}/api/employee", headers=headers, data=payload)

            # print(response.text)
            if response.status_code != 201:
                err.append(FCCODE)

            print(f"{i}.Sync Status Code:{response.status_code} DataID: {FCCODE}")
            i += 1
            # time.sleep(0.1)
            
        cursor.close()
        conn.close()
        print(f"============== Employee =============")
        print(err)
        print(f"=======================================")


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
        
def sync_product_group():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from PDGRP"""
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
                "POST", f"{urlAPI}/api/product_group", headers=headers, data=payload)

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
        
def sync_section():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from SECT"""
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
                "POST", f"{urlAPI}/api/section", headers=headers, data=payload)

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

def sync_department():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCCODE,FCNAME,FCNAME2 from DEPT"""
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
                "POST", f"{urlAPI}/api/department", headers=headers, data=payload)

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

def sync_book():
    response = requests.request("POST", f"{urlAPI}/api/token/", headers=objHeader, data=userLogIn)
    if response.status_code == 200:
        obj = response.json()
        token = obj['access']
        conn = pymssql.connect(host=dbHost, user=dbUser,password=dbPassword, charset=dbCharset, database=dbName, tds_version=r'7.0')
        SQL_QUERY = f"""select FCSKID,FCREFTYPE,FCCODE,FCNAME,FCNAME2,RTRIM(FCPREFIX) from BOOK order by FCREFTYPE,FCCODE"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCSKID = str(f"{r[0]}").strip()
            FCREFTYPE = str(f"{r[1]}").strip()
            FCCODE = str(f"{r[2]}").strip()
            FCNAME = str(f"{r[3]}").strip()
            FCNAME2 = str(f"{r[4]}").strip()
            FCPREFIX = str(f"{r[5]}")
            
            payload = f'skid={FCSKID}{FCREFTYPE}{FCCODE}&order_type_id={FCREFTYPE}&code={FCCODE}&name={FCNAME}&description={FCNAME2}&prefix={FCPREFIX}&is_active=1'.encode(
                'utf8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'}

            response = requests.request(
                "POST", f"{urlAPI}/api/book", headers=headers, data=payload)

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
        SQL_QUERY = f"""select p.FCSKID,p.FCTYPE,p.FCCODE,p.FCNAME,p.FCNAME2,g.FCCODE,u.FCCODE from PROD p inner join PDGRP g on p.FCPDGRP=g.FCSKID inner join UM u on p.FCUM=u.FCSKID where p.FCTYPE in ('1','5') order by p.FCCODE,p.FCNAME"""
        # SQL_QUERY = f"""select FCSKID,FCTYPE,FCCODE,FCNAME,FCNAME2 from PROD where FCCODE in ('50104-6006', '50502-529', '5T078-63911-06-D3', 'FDL4 1843', 'W9524-56411-03', 'W95EB-0004A')"""
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        err = []
        i = 1
        for r in cursor.fetchall():
            FCTYPE = str(f"{r[1]}").strip()
            FCCODE = str(f"{r[2]}").strip()
            FCNAME = str(f"{r[3]}").strip()
            FCNAME2 = str(f"{r[4]}").strip()
            FCPDGRP = str(f"{r[5]}").strip()
            FCUM = str(f"{r[6]}").strip()
            if len(FCNAME2) == 0:
                FCNAME2 = f"{FCCODE}-{FCNAME}"

            payload = f'prod_type_id={FCTYPE}&prod_group_id={FCPDGRP}&unit_id={FCUM}&code={FCCODE}&name={FCNAME}&description={FCNAME2}&is_active=1'.encode(
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
    sync_supplier()
    sync_employee()
    sync_product_type()
    sync_um()
    sync_order_type()
    sync_product_group()
    sync_section()
    sync_department()
    sync_book()
    sync_product()
