from sqlalchemy import create_engine, MetaData, Table, insert, func, select,text
from sqlalchemy.sql import and_, or_
from core import app


engine = create_engine(app.config['DATABASE_URI'],pool_size=32, max_overflow=64)

#creating a class User_details..
class BOModel():
    def __init__(self):
        try:
            self.meta = MetaData()
            self.bo_users = Table("bo_users", self.meta, autoload=True, autoload_with=engine)
            self.users = Table("users", self.meta, autoload=True, autoload_with=engine)
            self.halls = Table("halls", self.meta, autoload=True, autoload_with=engine)

        except Exception as e:
            print(e)

    def get_users_email_data(self,email,password):
        conn = engine.connect()
        stmt = self.bo_users.select().where(self.bo_users.c.email.in_([email])).where(self.bo_users.c.password.in_([password]))
        results = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in results] if results else None
        if results : 
            return results[0]
        else:
            return None
            
    def get_halls(self):
        conn = engine.connect()
        stmt = select([self.halls])
        result = conn.execute(stmt)
        conn.close()
        return result           
    def get_session_date(self):
        conn = engine.connect()
        stmt = text("select distinct(date) from sessions ;")
        result = conn.execute(stmt)
        conn.close()
        return result      

    def update_last_login(self,bo_user_id,last_login):
        conn = engine.connect()
        stmt = self.bo_users.update().values({"last_login":last_login}).where(self.bo_users.c.bo_user_id.in_([bo_user_id]))
        result = conn.execute(stmt)
        conn.close()
        return result

    def get_registered_data(self):
        conn = engine.connect()
        print('in Get Function')
        stmt = text("SELECT * FROM users order by user_id asc")
        result = conn.execute(stmt)
        conn.close()
        return result

    def get_registered_count(self):
        conn = engine.connect()
        print('in Get Function')
        stmt = text("SELECT COUNT(*)  as reg_count FROM users");
        results = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in results] if results else None
        if results : 
            return results[0]
        else:
            return None

    def sessionFilter(self,hall_search,date_search):
        conn = engine.connect()
        print("In model session filter Function")
        if hall_search and not date_search:
            stmt = text("select * from sessions where session_hall = "+ "'"+hall_search+"'" + "  order by date and session_start_date_time ;")
        if date_search and not hall_search:
            stmt = text("select * from sessions where date = "+ "'"+date_search+"'" + "  order by date and session_start_date_time ;")
        if not date_search and not hall_search:
            stmt = text("select * form sessons ;")
        else:
            stmt = text("select * from sessions where  session_hall = "+ "'"+hall_search+"'" + " and   date = "+ "'"+date_search+"'" + "  order by date and session_start_date_time ;")
               
        print(stmt)

        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        print(results)
        return results
        
    # send single mail 
    def getUserdataToMail(self,email):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.email.in_([email]))
        result = conn.execute(stmt)
        result = result.fetchone()
        conn.close()
        if result :
            return result
        else:
            return None              

        


    # def get_users_email_data(self,email):
    #     stmt = self.bo_users.select().where(self.bo_users.c.email.in_([email]))
    #     results = conn.execute(stmt)
    #     results = [dict(r) for r in results] if results else None
    #     if results : 
    #         return results[0]
    #     else:
    #         return None                     