#!/usr/bin/env python3
from sys import argv
from Controller import BackupController

argv=argv[1:]
ope=argv[0] if len(argv)>0 else None 
if(ope):
    controler=BackupController()
    if(ope=='drive'):
        print('Backup to drive')
        controler.backup_to_drive()
    if(ope=='local'):
        print('Backup to local database')
        controler.backup_to_local()
    if(ope=='sql'):
        print('Backup to sql file in sql/')
        controler.backup_to_sql()()
else :
    print('Syntax qlocal-backup <ope>')
    print('     drive: Downlaod & Upload backup to Gdrive')
    print('     local: Downlaod & Upload backup to a local database')
    print('     sql: Downlaod & Upload backup to sql file in sql/ folder')