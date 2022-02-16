class Config(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite:///:memory:'
    # DATABASE_URI = 'mysql+mysqldb://root:@127.0.0.1:3306/virtual_conference' #local db
    # DATABASE_URI = 'mysql+mysqldb://urbanedgeco_sposiconf:KXiTLJfk}8ZU@103.227.176.18/urbanedgeco_sposi_conf' # live db    
    # DATABASE_URI = 'mysql+mysqldb://admin:admin_123@database-2.cebwysbmrbmg.ap-southeast-1.rds.amazonaws.com/BOA_2021' # live db    

class ProductionConfig(Config):
    
    DATABASE_URI = 'mysql+mysqldb://urbanedgeco_tnoavconf:kYV(012koVpz@103.227.176.18:3306/urbanedgeco_tnoavconf' # local db    
    # DATABASE_URI = 'mysql+mysqldb://admin:admin123@database-1.cebwysbmrbmg.ap-southeast-1.rds.amazonaws.com/urbanedgeco_tnoavconf' # live db  FOR tnoa 2021  
    # DATABASE_URI = 'mysql+mysqldb://root:@127.0.0.1:3306/boa_conf_2021' # live db    
    # DATABASE_URI = 'mysql+mysqldb://urbanedgeco_boa2021:A*GhF2g]wgG1@103.227.176.18/urbanedgeco_boa2021' # live db    
#     DATABASE_URI = 'mysql+mysqldb://dbmasteruser:Admin_123@ls-230927e8a9b6c5eee0df1fe844e161491eedda2e.cmslfubz2w2r.ap-south-1.rds.amazonaws.com/BOA_2021' # live db    
    # DATABASE_URI = 'mysql+mysqldb://dbmasteruser:Admin_123@ls-230927e8a9b6c5eee0df1fe844e161491eedda2e.cmslfubz2w2r.ap-south-1.rds.amazonaws.com/BOA_2021' # live db    
    # DATABASE_URI = 'mysql+mysqldb://admin:admin_123@database-2.cebwysbmrbmg.ap-southeast-1.rds.amazonaws.com/BOA_2021' # live db    
    # SQLITE_DB_URI = 'sqlite:///sqlite_vc_1.db' # Sqlite db  
    # SQLITE_DB_URI = 'sqlite:///sqlite_vc_2.db' # Sqlite db    
     
    CACHE_TYPE  = 'NULL'
    UPLOAD_PATH  = 'images'
    SESSION_TYPE = 'filesystem'
    TIMEZONE     = 'Asia/Calcutta'
    # SQLALCHEMY_POOL_RECYCLE = <db_wait_timeout> - 1
    
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_GUN_KEY = 'DEVKEY23'

class SECRET_KEY(Config):
    SECRET_KEY = '5678906567890543346789976565'

