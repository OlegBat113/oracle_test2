# -*- coding: utf-8 -*-

import cx_Oracle
import os

# Oracle
con = None
cursor = None
oraError = None

def load_env(env_path='.env'):
    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def Connect_Oracle():
    global con, cursor, oraError
    print('Connect to Oracle ...')
    oraError = None

    # Использование:
    config = load_env()
    db = config['ORACLE_DB']
    user = config['ORACLE_USER']
    password = config['ORACLE_PASS']
    print(f'ORACLE: {user}@{db}')
    
    try:
        #print('ORACLE_HOME:',os.environ['ORACLE_HOME'])
        con = cx_Oracle.connect(user,password,db, encoding='UTF-8')
        print(f'ORACLE: Connected to {db}.')
        print('cx_Oracle version', con.version)
        cursor=con.cursor()
    except Exception as e:
        print('ORACLE Error:', e)
        oraError = e
        con = None
        cursor = None


def Close_Oracle():            
    global con, cursor
    if cursor is not None:
        cursor.close()
        con.close()
        print('ORACLE: Closed.')
    con=None
    cursor=None

def Get_Data():
    global con, cursor
    print('\n-> Get All Shops ... ----------------------------------')
    # Улан-Удэ
    s="select a.id, a.name, b.id as class_id, b.name as class_name, b.tree, nvl(a.floorspace, 0) as floor "
    s+=" from smstorelocations a"
    s+=" left join sastoreclass b on (b.id=a.idclass)"
    s+=" where (b.tree like '1.1.%')"
    s+=" order by a.name"
    print(f'SQL: {s}')
    cursor.execute(s)
    recs=cursor.fetchall()
    for rec in recs:
        print(rec)

    print('len(recs) =',len(recs))


Connect_Oracle()

print('cursor = ',cursor)
Get_Data()

Close_Oracle()
