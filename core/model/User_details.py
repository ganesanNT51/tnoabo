from sqlalchemy import create_engine, MetaData, Table, insert, func, select, bindparam
from sqlalchemy.sql import and_, or_
from core import app

engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)

#creating a class User_details..
class User_details():
    def __init__(self):
        try:
            self.meta = MetaData()
            self.users = Table("users", self.meta, autoload=True, autoload_with=engine)
            self.countries = Table("countries", self.meta, autoload = True, autoload_with = engine)
            self.states = Table("states", self.meta, autoload = True, autoload_with = engine)
            self.faculties = Table("faculties", self.meta, autoload=True, autoload_with=engine)

            self.help_desk = Table("help_desk", self.meta, autoload=True, autoload_with=engine)
        except Exception as e:
            print(e)

    def get_users_mem_no(self,mem_no):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.membership_no.in_([mem_no]))
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        if results :
            return results[0]
        else:
            return None

    def get_users_email(self,email):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.email.in_([email]))
        result = conn.execute(stmt)
        result = result.fetchone()
        conn.close()
        if result :
            return "success"
        else:
            return "fail"
    def get_users_email_data(self,email):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.email.in_([email]))
        results = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in results] if results else None
        if results : 
            return results[0]
        else:
            return None   

    def get_users_mobile_data(self,mobile):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.mobile.in_([mobile]))
        results = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in results] if results else None
        if results : 
            return results[0]
        else:
            return None          

    def get_users_mobile(self,mobile):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.mobile.in_([mobile]))
        result = conn.execute(stmt)
        result = result.fetchone()
        conn.close()
        if result :
            return "success"
        else:
            return "fail"

    def get_users_id(self,user_id):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        if results : 
            return results[0]
        else:
            return None

    def insert_users(self, data):
        conn = engine.connect()
        print('inside model insert cust')
        result = conn.execute(self.users.insert(), data)
        conn.close()
        return result

    def get_countries(self):
        conn = engine.connect()
        stmt = self.countries.select()
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        return results

    def get_states(self):
        conn = engine.connect()
        stmt = self.states.select()
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        return results

    # def get_states(self,id):
    #     stmt = self.states.select().where(self.states.c.country_id.in_([id]))
    #     result = conn.execute(stmt)
    #     results = [dict(r) for r in result] if result else None
    #     return results

    def update_users(self,id,data):
        conn = engine.connect()
        stmt = self.users.update().where(self.users.c.user_id.in_([id]))
        result = conn.execute(stmt,data)
        conn.close()
        return result

    def update_user_otp(self,user_id,otp,otp_created_at,otp_expiry_at):
        conn = engine.connect()
        stmt = self.users.update().values({"otp":otp, "otp_created_at":otp_created_at, "otp_expiry_at":otp_expiry_at}).where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        return result

    def update_last_login(self,user_id,last_login):
        conn = engine.connect()
        stmt = self.users.update().values({"last_login":last_login}).where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        return result    

    def get_state_and_country_names(self,user_id):
        conn = engine.connect()
        stmt = self.users.join(self.states, self.users.c.state == self.states.c.state_id).join(self.countries, self.users.c.country == self.countries.c.country_id)
        stmt = select([self.states.c.state_name, self.countries.c.name]).select_from(stmt).where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        return results[0]

    def update_password(self,user_id,password, confirm_password):
        conn = engine.connect()
        stmt = self.users.update().values({"password":password, "confirm_password":confirm_password}).where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        return result

    def edit_profile(self,id):
        conn = engine.connect()
        print('in Edit Function')
        stmt = select([self.users]).where(self.users.c.user_id.in_([id]))
        result = conn.execute(stmt)
        conn.close()
        output = result.fetchone()
        print(output.full_name)
        return output


    def get_faculty(self):
        conn = engine.connect()
        stmt = select([self.faculties])
        result = conn.execute(stmt)
        conn.close()
        return result

    def get_userdata(self,user_id):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        output = result.fetchone()
        return output   

    def insert_feedback(self, data):
        conn = engine.connect()
        print('inside model insert cust')
        result = conn.execute(self.help_desk.insert(), data)
        conn.close()
        return result

    def get_users(self):
        conn = engine.connect()
        print('in Get Function')
        stmt = select([self.users])
        result = conn.execute(stmt)
        conn.close()
        return result

    def update_mailsend_time(self,user_id,mail_send_at):
        conn = engine.connect()
        stmt = self.users.update().values({"mail_send_at":mail_send_at}).where(self.users.c.user_id.in_([user_id]))
        result = conn.execute(stmt)
        conn.close()
        return result

    def get_all_users(self):
        conn = engine.connect()
        stmt = select([self.users])
        results =  conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in results] if results else None
        return results      

    def bulk_update(self,data):
        conn = engine.connect()
        stmt =  self.users.update().\
                where(self.users.c.user_id == bindparam('_user_id')).\
                values({
                    'encrypt_user_id': bindparam('encrypt_user_id'),
                })
        
        conn.execute(stmt,data)
        conn.close()
        return "updated"      
        
    # send single mail 
    def getUserdataToMail(self,email):
        conn = engine.connect()
        stmt = self.users.select().where(self.users.c.email.in_([email]))
        #stmt = text("select * from users where email =  "+"'"+email+"'"+ "  and   email is not null; ")
        result = conn.execute(stmt)
        result = result.fetchone()
        conn.close()
        if result :
            return result
        else:
            return None                    