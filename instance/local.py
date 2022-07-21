server = 'localhost'
database = 'pos'
username = 'itm'
password = 'itm123'
port = '3306'
driver = 'MySQL ODBC 8.0 Unicode Driver'

SQLALCHEMY_DATABASE_URI = 'mysql://'+username+':'+password+'@'+server+':'+port+'/'+database+'?charset=utf8'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,  # Will make sure the connection is alive then perform real connect.
    'pool_recycle': 60,     # Should be lower than wait_timeout of mysql.
    'pool_timeout': 900,    # Number of seconds to wait before giving up on getting a connection from the pool
    'pool_size': 20,
    'max_overflow': 500,
    # 'isolation_level': 'READ COMMITTED' # Might cause flask app unstable, use it carefully.
}