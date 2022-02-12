#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import urllib.parse as urlparse
from datetime import datetime
from Gdrive import Drive
from pathlib import Path

class BackupController:
    config={
        "DATABASE_URL":None,
        "dbname_local" : None,
        "user_local" : None,
        "password_local" :None, 
        "host_local" :None,
        "port_local" : None,

        "dbname_heroku" : None,
        "user_heroku" : None,
        "password_heroku" : None,
        "host_heroku" : None,
        "port_heroku" : None
    }
    def __init__(self):
        try:
            self.config_env()    
            print('Configurando Env...PASSOU')
        except:
            print('Configurando Env...FALHOU')
    def config_env(self):
        #load dotenv
        load_dotenv('.env')
        env=os.environ
        #set config variables
        self.config["DATABASE_URL"]=env.get('DATABASE_URL')
        self.config["dbname_local"] = env.get('DB_DBNAME_LOCAL')
        self.config["user_local"] = env.get('DB_USER_LOCAL')
        self.config["password_local"] =env.get('DB_PASSWORD_LOCAL') 
        self.config["host_local"] = env.get('DB_HOST_LOCAL')
        self.config["port_local"] = env.get('DB_PORT_LOCAL')
        url= urlparse.urlparse(self.config["DATABASE_URL"])
        self.config["dbname_heroku"] = url.path[1:]
        self.config["user_heroku"] = url.username
        self.config["password_heroku"] = url.password
        self.config["host_heroku"] = url.hostname
        self.config["port_heroku"] = url.port
    def backup_to_drive(self):
        #create gdrive instance
        drive=Drive()
        #preparing new filename
        filename=self.generate_filename()
        #donwload database
        self.download_database()
        #restore dabatase to tmpfile
        self.restore_database_to_sql()
        #move and rename tmpfile to sql/filename
        os.replace('tmpfile.sql',f'sql/{filename}')
        #go to sql directory
        os.chdir('sql')
        #upload file to drive
        drive.UploadFile(filename)
        #go back to root
        os.chdir('../')
        #delete heroku dump
        os.remove('latest.dump')
    def download_database(self):
        URL=self.config["DATABASE_URL"]
        print('Downloading Database Dump...')
        os.system(f'pg_dump -F c --no-acl --no-owner --quote-all-identifiers {URL} --file latest.dump')
        print('Downloading Database Dump...PASSOU')
    def restore_database_to_sql(self):
        print('Dump to sql file...')
        os.system('pg_restore -f tmpfile.sql latest.dump')
        print('Dump to sql file...PASSOU')  
    def generate_filename(self):
        return f'backup({datetime.now().strftime("%d-%m-%Y")}).sql'
    def backup_to_sql(self):
        self.download_database()
        self.restore_database_to_sql()
        filename=self.generate_filename()
        #move and rename tmpfile to sql/filename
        os.replace('tmpfile.sql',f'sql/{filename}')
        os.remove('latest.dump')
    def backup_to_local(self):
        database_name=self.config["dbname_local"]
        user_name=self.config["user_local"]
        print(f'Backup to Local {database_name}...')
        self.download_database()
        os.system(f'psql {user_name} -c "drop database {database_name}"')
        os.system(f'psql {user_name} -c "create database {database_name} with owner {user_name}"')
        os.system(f'pg_restore --verbose --clean --no-acl --no-owner -h localhost -U {user_name} -d {database_name} latest.dump')
        print(f'Backup to Local {database_name}...PASSOU')
        os.remove('latest.dump')


