from flask import session
from sqlalchemy import create_engine, select, MetaData, Table, text,bindparam
from sqlalchemy.sql import and_, or_
from core import app

engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)


# engine = create_engine('')
class UserModel():  
    def __init__(self):
        try:
            self.meta = MetaData()
            self.users = Table("users", self.meta, autoload=True, autoload_with=engine)
        except Exception as e:
            print(e)

        

    def login(self,email,password):
        conn = engine.connect()
        stmt = select([self.users])
        stmt = stmt.where(
            and_(
                    self.users.c.email.in_([email]),
            and_(
                self.users.c.password.in_([password])
            )
            )
        )
        result = conn.execute(stmt)
        conn.close()
        print(result)
        results = [dict(r) for r in result] if result else None 
        # print(results)
        return results
    
    def getprime(self,email):
        conn = engine.connect()
        stmt = select([self.users])
        stmt = stmt.where(
            and_(
                    self.users.c.email.in_([email])
            )
        )
        result = conn.execute(stmt)
        conn.close()
        print(result)
        results = [dict(r) for r in result] if result else None
        # print(results)
        return results

    def getuser(self,user_id):
        conn = engine.connect()
        stmt = select([self.users])
        stmt = stmt.where(
            and_(
                    self.users.c.user_id.in_([user_id])
            )
        )
        result = conn.execute(stmt)
        conn.close()
        print(result)
        results = [dict(r) for r in result] if result else None
        # print(results)
        return results

    def login(self,email,password):
        conn = engine.connect()
        stmt = select([self.users])
        stmt = stmt.where(
            and_(
                    self.users.c.email.in_([email]),
            and_(
                self.users.c.password.in_([password])
            )
            )
        )
        result = conn.execute(stmt) 
        conn.close()
        # print(result)
        results = [dict(r) for r in result] if result else None 
        # print(results)
        return results

    def getalluser(self):
        conn = engine.connect()
        stmt = select([self.users])
        # stmt = stmt.where(
        #     and_(
        #           self.users.c.user_id.in_([user_id])
        #     )
        # )
        result = conn.execute(stmt)
        conn.close()
        # print(result)
        results = [dict(r) for r in result] if result else None
        # print(results)
        return results  

    def get_mobile(self,mobile):
        conn = engine.connect()
        stmt = select([self.users])
        stmt = stmt.where(
            and_(
                    self.users.c.mobile.in_([mobile])
            )
        )
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        return results
    
    
    
    def create_otp(self, data, mobile):
        conn = engine.connect()
        try:
            stmt = self.users.update()
            stmt = stmt.where(

                    self.users.c.mobile.in_([mobile])
            )
            result = conn.execute(stmt,data)
            conn.close()
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def create_otp_by_email(self, data, email, mobile):
        conn = engine.connect()
        try:
            stmt = self.users.update()
            stmt = stmt.where(
                    and_(
                    self.users.c.email.in_([email]),
                    self.users.c.mobile.in_([mobile])
                )
            )
            result = conn.execute(stmt,data)
            conn.close()
            return True
        except ClientError as e:
            logging.error(e)
            return False


    def otpverify(self, otp, data):
        conn = engine.connect()
        try:
            stmt = self.users.update()
            stmt = stmt.where(
                    and_(
                    self.users.c.otp.in_([otp])
                )
            )
            result = conn.execute(stmt,data)
            conn.close()
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def getuserid(self,user_id):
        conn = engine.connect()
        stmt = select([self.users])
        stmt = stmt.where(
            and_(
                    self.users.c.user_id.in_([user_id]) 
            )
        )
        result = conn.execute(stmt)
        conn.close()
        print(result)
        results = [dict(r) for r in result] if result else None
        # print(results)
        return results  

    def get_session(self):
        conn = engine.connect()
        stmt = select([self.users])
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        return results  

    def Auth(user):
        s_user = session.get('user')
        return  s_user


    # Sridhar , 2021-05-06 
    def get_commitment_list(self):
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("usp_commitment_list") # call store procedure name
            
            columns = [column[0] for column in cursor.description]
            # print(columns)
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
                # print(results)
            cursor.close()
            connection.commit()
        finally:
            connection.close() 
        return results  

    # Sridhar , 2021-05-07 
    def get_user_commitment(self,user_id):
        conn = engine.connect()
        stmt = text('select * from sessions s '
                    +' inner join authors a on a.session_id = s.session_id'
                    +' inner join users u on u.user_id = a.user_id'
                    +' inner join roles r on r.role_id = a.role_id'
                    +' where u.user_id =:user_id order by s.date,s.session_start_date_time,s.session_hall,r.order_no')
        result = conn.execute(stmt,user_id=user_id)
        print('panner id dt')
        print(result)
        results = [dict(r) for r in result] if result else None
        return results 

    # Sridhar , 2021-05-09
    def get_commitment_users_email(self,user_ids):
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("usp_commintment_mailer",[user_ids]) # call store procedure name
            
            columns = [column[0] for column in cursor.description]
            # print(columns)
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
                # print(results)
            cursor.close()
            connection.commit()
        finally:
            connection.close()     
        return results      

    

    # def getquizusers(self):
    #   stmt = select([self.users])
    #   # stmt = stmt.where(
    #     #     and_(
    #     #             self.users.c.user_id.in_([user_id])
    #     #     )
    #     # )
    #   result = conn.execute(stmt)
    #   # print(result)
    #   results = [dict(r) for r in result] if result else None
    #   # print(results)
    #   return results  

    # def confirm_password(self, data, otp):
    #   try:
    #       stmt = self.users.update()
    #       stmt = stmt.where(
    #               and_(
    #               self.users.c.otp.in_([otp]),
                    
    #           )
    #       )
    #       result = conn.execute(stmt,data)
    #       # return result.rowcount
    #       return True
    #   except ClientError as e:
    #       logging.error(e)
    #       return False

    # def create_otp(self, data, user_id):
    #   stmt = select([self.users.c.otp])
    #   stmt = stmt.where(

    #           self.users.c.user_id.in_([user_id])
    #   )
    #   result = conn.execute(stmt)
    #   results = [dict(r) for r in result] if result else None
    #   return results



    # def otpverify(self, now, user_id):
    #   stmt = self.users.update().values(otpverify=now)
    #   stmt = stmt.where(
    #       and_(
    #           self.users.c.user_id.in_([user_id])
    #       )
    #   )
    #   result = conn.execute(stmt)
    #   return result.rowcount