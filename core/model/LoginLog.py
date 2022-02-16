from flask import session
from sqlalchemy import create_engine, select, MetaData, Table, text,bindparam,desc
from sqlalchemy.sql import and_, or_
from core import app

engine = create_engine(app.config['SQLITE_DB_URI'])

class LoginLog():  
    def __init__(self):
        try:
            self.meta = MetaData()
            self.login_log = Table("login_log", self.meta, autoload=True, autoload_with=engine)
        except Exception as e:
            print(e)

        

    def insertlog(self,user_id,email,current_dt):
        conn = engine.connect()
        data = {'user_id':user_id,'email':email,'logged_on':current_dt}
                # self.login_log
        result = conn.execute(self.login_log.insert(), data)
        # stmt = "insert into login_log (user_id,email,logged_on) values (:user_id,:email,:logged_on)"
        # result = conn.execute(stmt,user_id=user_id,email=email,current_dt=current_dt)
        conn.close()
        return result
    


    def get_loginlogs(self):
        stmt = self.login_log.select().order_by(desc(self.login_log.c.logged_on))
        result = engine.execute(stmt)
        results = [dict(r) for r in result] if result else None
        return results

    