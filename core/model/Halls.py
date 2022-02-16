from sqlalchemy import create_engine, MetaData, Table, insert, select,update,delete,text
from sqlalchemy.sql import and_, or_, distinct
from core import app
import datetime
from datetime  import datetime,date, timedelta,time
import json
import collections


engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)


class Halls():
    def __init__(self):
        try:
            self.meta = MetaData()
            self.halls = Table("halls", self.meta, autoload=True, autoload_with=engine)
            
            # self.abstracts = Table("abstracts", self.meta, autoload=True, autoload_with=engine)
            # self.categories = Table("categories", self.meta, autoload=True, autoload_with=engine)
            # self.authors = Table("authors", self.meta, autoload=True, autoload_with=engine)
        except Exception as e:
            print(e)
    

    # Author: BALAJI RAJ I START
    def get_halls(self):        
        stmt            =   select([self.halls.c.hall])
        data            =   engine.execute(stmt)
        
        # create list of dictionary        
        res             =   [dict(r) for r in data] if data else None        
        Result          =   [ sub['hall'] for sub in res ]
        Result          =   sorted(Result)                        
        
        return Result

    