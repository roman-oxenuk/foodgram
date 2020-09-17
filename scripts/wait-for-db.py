import os
import time

import psycopg2


dbname = os.environ.get('POSTGRES_DB')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

print('Connecting to')
print(f'host: {host}')
print(f'port: {port}')
print(f'dbname: {dbname}')
print(f'user: {user}')
print(f'password: {password}')


def try_to_connect():
    print('Trying to connect...')
    retry_after = 1
    try:
        psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except psycopg2.OperationalError:
        print(f'Failed. Retry after {retry_after} seconds.')
        time.sleep(retry_after)
        try_to_connect()
    else:
        print('Success.')

try_to_connect()
