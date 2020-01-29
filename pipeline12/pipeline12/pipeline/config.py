
USERNAME = 'wayne'
PASSWORD = 'wayne'
DBIP = '192.168.142.140'
DBPORT = 3306
DBNAME = 'pipeline'

DATABASE_DEBUG = True


URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, DBIP, DBPORT,
    DBNAME
)






















