# configs.py
def getConfigDB():
    configDB = {}
    configDB['host'] = 'localhost'
    configDB['user'] = 'root'
    configDB['port'] = '3306'       
    configDB['password'] = 'Lagarufa1806'
    configDB['database'] = 'bdGRPC'
    configDB['auth_plugin'] = 'mysql_native_password'
    
    return configDB
