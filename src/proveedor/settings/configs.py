# configs.py
def getConfigDB():
    configDB = {}
    configDB['host'] = 'localhost'
    configDB['user'] = 'root'
    configDB['port'] = '3306'
    configDB['pool_size'] = 30  
    configDB['password'] = 'root'
    configDB['database'] = 'bdKafka'
    configDB['auth_plugin'] = 'mysql_native_password'
    
    return configDB

def getConfigServerDB():
    configDB = {}
    configDB['host'] = 'localhost'
    configDB['user'] = 'root'
    configDB['port'] = '3306' 
    configDB['pool_size'] = 30        
    configDB['password'] = 'root'
    configDB['database'] = 'bdgrpc'
    configDB['auth_plugin'] = 'mysql_native_password'
    
    return configDB