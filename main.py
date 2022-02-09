#!/usr/bin/python3
import psycopg2
import os
from dotenv import load_dotenv
import urllib.parse as urlparse
from datetime import datetime
#config env
config = load_dotenv(".env")
env=os.environ;
APP_NAME=env.get("APP_NAME");
DATABASE_URL=env.get('DATABASE_URL')
#Split DATABASE_URL
url = urlparse.urlparse(DATABASE_URL)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

class BackupController:
    connection=None
    def __init__(self):
        self.connection=psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    def test(self):
        conn=self.connection
        cur = conn.cursor()
        cur.execute("SELECT * FROM categoria")
        records = cur.fetchall()
        print(records)
    def backup(self):
        today_date=datetime.now();
        filename=f'{today_date}.sql'
        os.system(f'heroku pg:backups:capture -a {APP_NAME}')
        os.system(f'heroku pg:backups:download -a {APP_NAME}')
        os.system('pg_restore -f tmpfile.sql latest.dump');   
        os.system(f'mv "./tmpfile.sql"  "./sql/{filename}"');
        os.system('rm latest.dump');






#Make CLI controller
control=BackupController() 
control.backup()
