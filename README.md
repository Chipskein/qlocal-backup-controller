# qlocal-backup-controller
### Description
Cli to automate heroku database backup and upload to gdrive,or local database,or sql file
creating using pg_dump and pg_restore insted of heroku-cli tools
#### Warning 
**Postgres need to be installed because this cli uses pg_dump and pg_restore**

### How config
Put a google drive credentials.json in root directory and create a .env file as in .env.example
### How to use
Just run ./qlocal_backup.py passing one of operation below
|||
| ------- | ---  |
| **drive** |   *Download & Upload backup to Gdrive* |
| **local** |  *Download & Upload backup to a local database* |
| **sql**   |  *Download & Upload backup to sql file in sql/ folder* |


### Necessary Python dependencies
* python-dotenv
* google-api-python-client 
* google-auth-httplib2 
* google-auth-oauthlib
