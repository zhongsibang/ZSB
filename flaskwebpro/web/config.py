USERNAME = 'xw'
PASSWORD = 'xw'
DBIP = '127.0.0.1'
DBPORT = 3306
DBNAME = 'pipeline'

URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD,
                    DBIP, DBPORT, DBNAME)

DATABASE_DEBUG = True


