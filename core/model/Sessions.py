from sqlalchemy import create_engine, MetaData, Table, insert, select,update,delete,text
from sqlalchemy.sql import and_, or_, distinct
from core import app
import datetime
from datetime  import datetime,date, timedelta,time
import json
import collections


# engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)
engine = create_engine(app.config['DATABASE_URI'])

class Sessions():
    def __init__(self):
        try:
            self.meta = MetaData()
            self.sessions = Table("sessions", self.meta, autoload=True, autoload_with=engine)
            self.comments = Table("comments", self.meta, autoload=True, autoload_with=engine)
            self.users = Table("users", self.meta, autoload=True, autoload_with=engine)
            self.s_attendance = Table("s_attendance", self.meta, autoload=True, autoload_with=engine)
            self.users_answer = Table("users_answer", self.meta, autoload=True, autoload_with=engine)
            
            # self.abstracts = Table("abstracts", self.meta, autoload=True, autoload_with=engine)
            # self.categories = Table("categories", self.meta, autoload=True, autoload_with=engine)
            # self.authors = Table("authors", self.meta, autoload=True, autoload_with=engine)
        except Exception as e:
            print(e)
    

    # Author: BALAJI RAJ I START
    def get_halls(self):       
        conn = engine.connect() 
        stmt            =   select([self.sessions.c.session_hall]).distinct()
        stmt            =   stmt.where(
                                self.sessions.c.session_hall.isnot(None)
                            )                        
        data            =   conn.execute(stmt)
        conn.close()
        # create list of dictionary        
        res             =   [dict(r) for r in data] if data else None        
        Result          =   [ sub['session_hall'] for sub in res ]
        Result          =   sorted(Result)                        
        
        return Result

    def fetchallsession(self, progdate, searchtxt, searchhall):
        conn = engine.connect()
        Result      = None        
        dates       = None
        hall        = None
        message     = None
       
        stmt                =   select([self.sessions])
        if progdate:
            stmt            =   stmt.where(self.sessions.c.date.in_(progdate))
        if searchtxt:
            stmt            =   stmt.where(self.sessions.c.session_title.like(searchtxt))            
        if searchhall:
            stmt            =   stmt.where(self.sessions.c.session_hall.in_(searchhall))                                            
        
        data                =   conn.execute(stmt)
        conn.close()
        Result              =   [dict(r) for r in data] if data else None
        print(Result)               
        
        return {'Result':Result,'message':message}
    
    def insert_session(self, data):
        conn = engine.connect()
        result = conn.execute(self.sessions.insert(), data)
        conn.close()
        session_id = [r for r in result.inserted_primary_key] if result.inserted_primary_key else None
        print(session_id)
        return session_id

    def update_session(self, data, id):
        conn = engine.connect()
        stmt = self.sessions.update()
        stmt = stmt.where(
			and_(
				self.sessions.c.session_id.in_([id]),
			)
		)
        result = conn.execute(stmt,data)
        conn.close()
        return result.rowcount
    
    def delete_session(self, id):
        conn = engine.connect()
        stmt = self.sessions.delete()
        stmt = stmt.where(
			and_(
				self.sessions.c.session_id.in_([id]),
			)
		)
        result = conn.execute(stmt)
        conn.close()
        message         =   'Session successfully deleted!'        
        return message

    def get_progdates(self):
        conn = engine.connect()
        stmt            =   select([self.sessions.c.date]).distinct()
        stmt            =   stmt.where(
                                self.sessions.c.date.isnot(None)
                            )
        data            =   conn.execute(stmt)
        conn.close()
        # create list of dictionary        
        res             =   [dict(r) for r in data] if data else None        
        progdates       =   [ sub['date'] for sub in res ]
        progdates       =   sorted(progdates)
        # print(progdates[0])
        return progdates

    def checkdate(self,progdate):
        conn = engine.connect()
        stmt            =   select([self.sessions.c.date])
        stmt            =   stmt.where(
                                self.sessions.c.date.in_([progdate])
                            )
        result          =   conn.execute(stmt)
        conn.close()
        temp            =   [dict(r) for r in result] if result else None        
        return temp     

    def get_all_halls(self, progdate):
        conn = engine.connect()
        stmt            =   select([self.sessions.c.session_hall]).distinct()                
        stmt            =   stmt.where(
                                self.sessions.c.date.in_([progdate])
                            )
        data            =   conn.execute(stmt)
        conn.close()
        
        # remove duplicates -- commented since we have now used distinct() in query
        # xaxis_list  =   []        
        # [xaxis_list.append(i) for i in data if i not in xaxis_list]        
        
        # create list of dictionary        
        res             =   [dict(r) for r in data] if data else None        
        Result          =   [ sub['session_hall'] for sub in res ]
        Result          =   sorted(Result)                        
        
        return Result


    def get_data(self, progdate, searchtxt, searchhall):
        conn = engine.connect()
        # print('model :'+searchhall)
        Result      = None
        daystart    = None
        dayend      = None
        dictList    = None
        dates       = None
        hall        = None
        message     = None


        stmt                =   select([self.sessions]).where(self.sessions.c.date.in_([progdate]))
        if searchtxt:
            stmt            =   stmt.where(self.sessions.c.session_title.like(searchtxt))            

        if searchhall:
            stmt            =   stmt.where(self.sessions.c.session_hall.in_(searchhall))                                
        
        data                =   conn.execute(stmt)
        conn.close()
        Result              =   [dict(r) for r in data] if data else None        
        # print('model result:'+str(Result))
        
        if Result:
            # print('Hi result exists')
            hall            =   []

            # print('Result before model : '+ str(Result))
            for sub in Result:
                if sub['session_hall'] not in hall:
                    hall.append(sub['session_hall'])
            hall            =   sorted(hall)
            # print('Result after model : '+ str(Result))
            
            start           =   [ r['session_start_date_time'] for r in Result ]
            end             =   [ r['session_end_date_time'] for r in Result ]
            # print('model : '+ str(start))
            #get daystarttime
            starttime_list  =   []                
            [starttime_list.append(i.time().strftime('%H:%M')) for i in start if i.time().strftime('%H:%M') not in starttime_list]
            starttime_list  =   sorted(starttime_list)
            daystart        =   starttime_list[0]        

            #get dayendtime
            endtime_list    =   []
            for i in end:            
                endtime_list.append(i.time().strftime('%H:%M'))        
            endtime_list    =   sorted(endtime_list, reverse=True)
            dayend          =   endtime_list[0]

            # split time into 5 min intervals betweeen daystart and dayend
            fmt             =   '%H:%M'
            d1              =   datetime.strptime(daystart, fmt)        
            d2              =   datetime.strptime(dayend, fmt)
            delta           =   timedelta(minutes=15)
            yaxis           =   []
            while d1 < d2:
                yaxis.append(d1.strftime("%H:%M"))
                d1          +=   delta            
            yaxis.append(d2.strftime("%H:%M"))

            # create y axis values
            data            =   []
            for i in range(len(yaxis) - 1):
                # result = "{} - {}".format(times[i], times[i+1])
                result      =    [yaxis[i], yaxis[i+1]]
                data.append(result)                
            yaxis           =   [] 
            [yaxis.append(x) for x in data if x not in yaxis]  
            # print('>> yaxis <<')
            # print(yaxis)

            # create a list of dictionaries
            keys            =   ['Starttime', 'Endtime']        
            dictList        =   []
            dictList        =   collections.OrderedDict
            dictList        =   [{k:v for k,v in zip(keys, y)} for y in yaxis]
            #print('>> dictList <<')
            #print(dictList)
        else: 
            Result          =   None   
            message         =   'Data unavailable, try changing search text or the hall. Click here to go back to programsheet.'

        return {'Result':Result,'daystart':daystart,'dayend':dayend,'dictList':dictList,'hall':hall,'message':message}

    def get_dates(self):
        conn = engine.connect()
        stmt            =   select([self.sessions.c.date]).distinct()
        stmt            =   stmt.where(
                                self.sessions.c.date.isnot(None)
                            )
        data            =   conn.execute(stmt)
        conn.close()
        # create list of dictionary        
        res             =   [dict(r) for r in data] if data else None        
        dates           =   [ sub['date'] for sub in res ]
        dates           =   sorted(dates)
        # dates           =   str(dates)                        
        # print('>> dates <<')
        # print(dates)
        # print(len(start))
        return dates

        
        
    def get_activesessions_data(self, progdate, searchtxt, searchhall):
        conn = engine.connect()
        # print('model :'+searchhall)
        dt = datetime.now()
        stmt                =   select([self.sessions])        
        stmt                =   stmt.where(
                            and_(
                                    self.sessions.c.date.in_([progdate]),
                            and_(
                                    self.sessions.c.session_start_date_time <= dt,
                            and_(
                                    self.sessions.c.session_end_date_time >= dt
                                )
                                )
                                )
                            )
        if searchtxt:
            stmt            =   stmt.where(self.sessions.c.session_title.like(searchtxt))            
        if searchhall:
            stmt            =   stmt.where(self.sessions.c.session_hall.in_(searchhall))                                
        
        data                =   conn.execute(stmt)
        Result              =   [dict(r) for r in data] if data else None        
        # print('model result:'+str(Result))        

        if not Result:            
            Message         =   'Data unavailable: No active sessions at this time.'
            # print(Message)
            return {'Message':Message}

        if Result:
            # print('Hi result exists')
            hall            =   []

            # print('Result before model : '+ str(Result))
            for sub in Result:
                if sub['session_hall'] not in hall:
                    hall.append(sub['session_hall'])
            hall            =   sorted(hall)
            # print('Result after model : '+ str(Result))
            
            start           =   [ r['session_start_date_time'] for r in Result ]
            end             =   [ r['session_end_date_time'] for r in Result ]
            # print('model : '+ str(start))
            #get daystarttime
            starttime_list  =   []                
            [starttime_list.append(i.time().strftime('%H:%M')) for i in start if i.time().strftime('%H:%M') not in starttime_list]
            starttime_list  =   sorted(starttime_list)
            daystart        =   starttime_list[0]        

            #get dayendtime
            endtime_list    =   []
            for i in end:            
                endtime_list.append(i.time().strftime('%H:%M'))        
            endtime_list    =   sorted(endtime_list, reverse=True)
            dayend          =   endtime_list[0]

            # split time into 5 min intervals betweeen daystart and dayend
            fmt             =   '%H:%M'
            d1              =   datetime.strptime(daystart, fmt)        
            d2              =   datetime.strptime(dayend, fmt)
            delta           =   timedelta(minutes=15)
            yaxis           =   []
            while d1 < d2:
                yaxis.append(d1.strftime("%H:%M"))
                d1          +=   delta            
            yaxis.append(d2.strftime("%H:%M"))

            # create y axis values
            data            =   []
            for i in range(len(yaxis) - 1):
                # result = "{} - {}".format(times[i], times[i+1])
                result      =    [yaxis[i], yaxis[i+1]]
                data.append(result)                
            yaxis           =   [] 
            [yaxis.append(x) for x in data if x not in yaxis]  
            # print('>> yaxis <<')
            # print(yaxis)

            # create a list of dictionaries
            keys            =   ['Starttime', 'Endtime']        
            dictList        =   []
            dictList        =   collections.OrderedDict
            dictList        =   [{k:v for k,v in zip(keys, y)} for y in yaxis]
            # print('>> dictList <<')
            # print(dictList)

            stmt            =   select([self.sessions.c.date]).distinct()
            data            =   conn.execute(stmt)
            conn.close()
            
            # create list of dictionary        
            res             =   [dict(r) for r in data] if data else None        
            dates           =   [ sub['date'] for sub in res ]
            dates           =   sorted(dates)
            # dates           =   str(dates)                        
            # print('>> dates <<')
            # print(dates)
            # print(len(start))
            Message         =   ''
            return {'Result':Result,'daystart':daystart,'dayend':dayend,'dictList':dictList,'dates':dates,'hall':hall,'Message':Message}



    def get_hallstarttime(self, progdate, hall):
        conn = engine.connect()
        stmt        =   select([self.sessions]).where(self.sessions.c.date.in_([progdate])).where(self.sessions.c.session_hall.in_([hall]))        
        data        =   conn.execute(stmt)
        conn.close()
        Result      =   [dict(r) for r in data] if data else None
        
        start       =   [ r['session_start_date_time'] for r in Result ]
        end         =   [ r['session_end_date_time'] for r in Result ]
        
        starttime_list  =   []                
        [starttime_list.append(i.time().strftime('%H:%M')) for i in start if i.time().strftime('%H:%M') not in starttime_list]
        starttime_list  =   sorted(starttime_list)
        # print('>> starttime_list from model<<')
        # print(starttime_list)   
        return starttime_list        
    
    # def get_progdate(self):        
    #     stmt        =   select([self.sessions.c.date]).distinct()
    #     data        =   conn.execute(stmt)
        
    #     # create list of dictionary        
    #     res         =   [dict(r) for r in data] if data else None        
    #     Result      =   [ sub['date'] for sub in res ]
    #     Result      =   sorted(Result)                        
    #     print('>> Result <<')
    #     print(Result)
    #     return Result
    
    # Author: BALAJI RAJ I END-------------------

    
    # Author: NANDHINI  START-------------------
    def getSessionId(self,session_id):
        conn = engine.connect()
        # current_time = time(now.hour, now.minute, now.second)
        dt = datetime.now()
        stmt = select([self.sessions])
        stmt = stmt.where(
            and_(
                    self.sessions.c.session_id.in_([session_id]),
            # and_(
            #         self.sessions.c.session_start_date_time <= dt,
            # and_(
            #         self.sessions.c.session_end_date_time >= dt
            #     )
            #     )
                )
            )
        results = conn.execute(stmt)
        
        # print(results)
        # result = [dict(r) for r in results] if results else None
        result = results.fetchone()
        conn.close()
        # print(result)
        return dict(result)


    def getCurrentSession(self):
        conn = engine.connect()
        # current_time = time(now.hour, now.minute, now.second)
        dt = datetime.now()
        stmt = select([self.sessions])
        stmt = stmt.where(
            and_(
                    self.sessions.c.session_start_date_time <= dt,
            and_(
                    self.sessions.c.session_end_date_time >= dt
                )
                )
            )
        results = conn.execute(stmt)
        conn.close()
        # print(results)
        # result = [dict(r) for r in results] if results else None
        result = results.fetchone()
        # print('**********result**********')
        # print(result)
        return  dict(result) if result else None



    def getCurrentSession_by_date(self,s_date):
        conn = engine.connect()
        # current_time = time(now.hour, now.minute, now.second)
        dt = datetime.now()
        stmt = select([self.sessions])
        stmt = stmt.where(
            and_(
                    self.sessions.c.session_start_date_time <= dt,
            and_(
                    self.sessions.c.session_end_date_time >= dt,
            and_(
                    self.sessions.c.date == s_date
                )
                )
                )
            )
        results = conn.execute(stmt)
        conn.close()
        # print(results)
        # result = [dict(r) for r in results] if results else None
        result = results.fetchone()
        # print('**********result**********')
        # print(result)
        return  dict(result) if result else None

    def getCurrentSession_by_date_hall(self,s_date,s_hall):
        conn = engine.connect()
        # current_time = time(now.hour, now.minute, now.second)
        dt = datetime.now()
        stmt = select([self.sessions])
        stmt = stmt.where(
            and_(
                    self.sessions.c.session_start_date_time <= dt,
            and_(
                    self.sessions.c.session_end_date_time >= dt,
            and_(
                    self.sessions.c.date == s_date,
            and_(
                    self.sessions.c.session_hall == s_hall        
                )
                )
                )
                )
            )
        results = conn.execute(stmt)
        conn.close()
        # print(results)
        # result = [dict(r) for r in results] if results else None
        result = results.fetchone()
        # print('**********result**********')
        # print(result)
        return  dict(result) if result else None    

    def previous_upcoming_session(self,dt):
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc('pre_upcom_sessions', [dt])
            columns = [column[0] for column in cursor.description]
            previous_ses = []
            for row in cursor.fetchall():
                previous_ses.append(dict(zip(columns, row)))
                # print('previous_ses')
                # print(previous_ses)
            cursor.nextset()  
            columns = [column[0] for column in cursor.description]  
            upcoming_ses = []
            for row in cursor.fetchall():
                upcoming_ses.append(dict(zip(columns, row)))
            cursor.close()
            connection.commit()
        finally:
            connection.close() 
        
        return {'previous_ses': previous_ses,'upcoming_ses':upcoming_ses}
        

    def getallsession(self):
        conn = engine.connect()
        stmt = select([self.sessions])
        result = conn.execute(stmt)
        conn.close()
        results = [dict(r) for r in result] if result else None
        return results

    def getSession(self,session_id):
        conn = engine.connect()
        stmt = select([self.sessions])
        stmt = stmt.where(
            and_(
                	self.sessions.c.session_id.in_([session_id])
            )
        )
        results = conn.execute(stmt)
        conn.close()
        result = [dict(r) for r in results] if results else None
		# print(results)
        return result

    def save_comment(self,comment_data):
        conn = engine.connect()
        result = conn.execute(self.comments.insert(),comment_data)
        conn.close()
        # print('save comment')
        # print(result)
        return result

    def getcomment(self,session_id):
        conn = engine.connect()
        stmt = self.comments.outerjoin(self.users, self.users.c.user_id == self.comments.c.user_id)
        stmt = select([self.comments,self.users.c.prefix,self.users.c.full_name]).order_by(self.comments.c.created_at).select_from(stmt).where(
            and_(
                	self.comments.c.session_id.in_([session_id])
            )
        )
        results = conn.execute(stmt)
        conn.close()
        # print(results)
        result = [dict(r) for r in results] if results else None
        return result

    def getcomment_by_date_hall(self,s_date,s_hall):
        conn = engine.connect()
        stmt = text('select c.created_at, u.*,c.* from comments c join sessions s on s.session_id = c.session_id join users u on u.user_id =c.user_id where s.date = :s_date and s.session_hall = :s_hall and c.is_reject = 0 order by c.created_at')
        results = conn.execute(stmt,s_date=s_date,s_hall=s_hall)
        conn.close()
        # print(results)
        result = [dict(r) for r in results] if results else None
        return result    

  

    def get_last_comment_dt(self,session_id):
        conn = engine.connect()
        stmt = text('select created_at from comments where session_id = :session_id and comments.is_reject =0 order by created_at desc limit 1')
        result = conn.execute(stmt,session_id=session_id)
        conn.close()
        output = result.fetchone()
        # print(results)
        return output

    def get_last_comment_dt_by_date_hall(self,s_date,s_hall):
        conn = engine.connect()
        stmt = text('select c.created_at from comments c join sessions s on s.session_id = c.session_id  where  s.date = :s_date and s.session_hall= :s_hall and c.is_reject = 0 order by c.created_at desc limit 1')
        result = conn.execute(stmt,s_date=s_date,s_hall=s_hall)
        conn.close()
        output = result.fetchone()
        # print(results)
        return output    


    def get_last_comments(self,msg_last_dt,session_id):
        conn = engine.connect()
        stmt = text("select comments.*,users.prefix,users.full_name FROM comments INNER JOIN users ON users.user_id = comments.user_id WHERE comments.created_at > :msg_last_dt AND comments.session_id IN (:session_id) and comments.is_reject = 0  order by created_at")
        results = conn.execute(stmt,msg_last_dt=msg_last_dt,session_id=session_id)
        conn.close()
        result = [dict(r) for r in results] if results else None
        # print(results)
        return result

    def get_last_comments_by_date_hall(self,msg_last_dt,s_date,s_hall):
        conn = engine.connect()
        stmt = text("select comments.*,users.prefix,users.full_name FROM comments inner join sessions s on s.session_id = comments.session_id INNER JOIN users ON users.user_id = comments.user_id WHERE comments.created_at > :msg_last_dt AND s.date = :s_date and s.session_hall = :s_hall and comments.is_reject = 0 order by comments.created_at")
        results = conn.execute(stmt,msg_last_dt=msg_last_dt,s_date=s_date,s_hall=s_hall)
        conn.close()
        result = [dict(r) for r in results] if results else None
        # print(results)
        return result    

   
    def get_abstract(self):
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("usp_test")
            
            columns = [column[0] for column in cursor.description]
            # print(columns)
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
                print(results)
            cursor.close()
            connection.commit()
        finally:
            connection.close()     
        # print(type(results))
        return results


    def session_attendance(self,data):
        conn = engine.connect()
        result = conn.execute(self.s_attendance.insert(),data)
        conn.close()
        # print('save att')
        # print(result)
        return result

    def session_close_time(self, data, session_id, user_id):
        conn = engine.connect()
        stmt = self.s_attendance.update()
        stmt = stmt.where(
            and_(
                self.s_attendance.c.session_id.in_([session_id]),
            and_(
                self.s_attendance.c.user_id.in_([user_id]),
            and_(
                self.s_attendance.c.close_time == None
            )
            )
            )       
        )
        result = conn.execute(stmt,data)
        conn.close()
        return result

    def get_s_att(self,session_id):
        conn = engine.connect()
        stmt = select([self.s_attendance])
        stmt = stmt.where(
            and_(
				self.s_attendance.c.session_id.in_([session_id]) 
			)
		)
        result = conn.execute(stmt)
        conn.close()
        # print(result)
        results = [dict(r) for r in result] if result else None
        # print(results)
        return {'session_att': results}   

    def nextsession(self,session_date_time):
        conn = engine.connect()
        stmt = text('select * from sessions s where session_start_date_time > :session_date_time order by session_start_date_time asc limit 1')
        result = conn.execute(stmt,session_date_time=session_date_time)
        conn.close()
        output = result.fetchone()
        # print(results)
        return output

    def get_debate(self,session_id):
        conn = engine.connect()
        dt = datetime.now()
        stmt = text('select * from s_debate where session_id=:session_id and :dt between start_time and end_time;')
        results = conn.execute(stmt,session_id=session_id,dt=dt)
        conn.close()
        result = results.fetchone()
        s_debate = dict(result) if result else None
        debate_options = None
        if s_debate:
            stmt = text('select * from debate_option where s_d_id=:s_d_id;')
            results1 = conn.execute(stmt,s_d_id=s_debate.get('s_d_id'))
            debate_options = [dict(r) for r in results1] if results1 else None
        return debate_options

    def user_answer(self,data):
        conn = engine.connect()
        result = conn.execute(self.users_answer.insert(),data)
        conn.close()
        # print('save att')
        # print(result)
        return result

    # def getpreupcomsession(self):
    #     stmt = text('select distinct date from sessions order by date')
    #     result = conn.execute(stmt)
    #     results = [dict(r) for r in result] if result else None
    #     # print(results)
    #     return results

    def getsessiondate(self,s_date):
        conn = engine.connect()
        stmt = text('select * from sessions where date = :s_date order by session_id limit 1')
        result = conn.execute(stmt,s_date=s_date)
        conn.close()
        # output = result.fetchone()
        # return output
        results = [dict(r) for r in result] if result else None
        # print('results***********')
        # print(results)
        return results

    def getSessionDateHall(self,s_date,s_hall):
        conn = engine.connect()
        stmt = text('select * from sessions where live_stream is not null and date = :s_date and session_hall= :s_hall order by session_id limit 1')
        result = conn.execute(stmt,s_date=s_date,s_hall=s_hall)
        conn.close()
        # output = result.fetchone()
        # return output
        results = [dict(r) for r in result] if result else None
        # print('results***********')
        # print(results)
        return results    

    def getSessionDates(self):
        conn = engine.connect()
        stmt = text('select distinct date from sessions where live_stream is not null order by date')
        result = conn.execute(stmt)
        conn.close()
        # output = result.fetchone()
        # return output
        results = [dict(r) for r in result] if result else None
        # print('results***********')
        # print(results)
        return results

    def getSessionHalls(self,s_date):
        conn = engine.connect()
        print("call")
        # engine.dispose()
        stmt = text('select distinct session_hall,date from sessions where live_stream is not null and date = :s_date order by session_hall')
        result = conn.execute(stmt,s_date=s_date)
        conn.close()
        conn.close()
        # output = result.fetchone()
        # return output

        results = [dict(r) for r in result] if result else None
        # print('results***********')
        # print(results)
        return results


    def getSessionPrevDates(self,s_date):
        conn = engine.connect()
        stmt = text('select distinct date from sessions where live_stream is not null and date < :s_date order by date')
        result = conn.execute(stmt,s_date=s_date)
        conn.close()
        # output = result.fetchone()
        # return output
        results = [dict(r) for r in result] if result else None
        # print('results***********')
        # print(results)
        return results    


    def getSessionNextDates(self,s_date):
        conn = engine.connect()
        stmt = text('select distinct date from sessions where live_stream is not null and date > :s_date order by date')
        result = conn.execute(stmt,s_date=s_date)
        conn.close()
        # output = result.fetchone()
        # return output
        results = [dict(r) for r in result] if result else None
        # print('results***********')
        # print(results)
        return results 

    def getbanner(self,banner_id,session_id):
        conn = engine.connect()
        stmt = text('select * from adv_banner where is_active=1 and banner_id>:banner_id and session_id=:session_id order by banner_id limit 1')
        result = conn.execute(stmt,banner_id=banner_id,session_id=session_id)
        conn.close()
        # print('panner id dt')
        # print(result)
        results = [dict(r) for r in result] if result else None
        return results 

    # def getallbanner(self):
    #     conn = engine.connect()
    #     stmt = text('select * from adv_banner where is_active=1 order by banner_id')
    #     result = conn.execute(stmt,banner_id=banner_id,session_id=session_id)
    #     conn.close()
    #     # print('panner id dt')
    #     # print(result)
    #     results = [dict(r) for r in result] if result else None
    #     return results 


    def getbannercount(self,session_id):
        conn = engine.connect()
        stmt = text('select count(*) as count from adv_banner where is_active=1 and session_id=:session_id;')
        result = conn.execute(stmt,session_id=session_id)
        conn.close()
        # print('panner id dt')
        # print(result)
        results = [dict(r) for r in result] if result else None
        return results     


    #      def CheckChatRoom(self,user_id,to_user_id):
    #    print('in getChatUsers Function')
    #    stmt = text('select * from chat c where (user_id = :user_id and to_user_id = :to_user_id) or (user_id = :to_user_id and to_user_id = :user_id)')
    #    result = conn.execute(stmt,user_id=user_id,to_user_id=to_user_id)
    #    output = result.fetchone()
    #    print(output)
    #    return output
        






        
    #     connection = engine.raw_connection()
    #     try:
    #         cursor = connection.cursor()
    #         cursor.callproc("usp_get_abstracts", [session_id])
    #         results = list(cursor.fetchall())
    #         # print(results)
    #         cursor.close()
    #         connection.commit()
    #     finally:
    #         connection.close()
    #     return results

    # def get_abstracts(self,session_id):
    #     connection = engine.raw_connection()
    #     cursor = connection.cursor()
    #     cursor.callproc('usp_get_abstracts', [session_id])
    #     columns = [column[0] for column in cursor.description]
    #     # print results
    #     # print("Printing laptop details")
    #     results_sess = []
    #     for row in cursor.fetchall():
    #         results_sess.append(dict(zip(columns, row)))
    #     cursor.nextset()  
    #     columns = [column[0] for column in cursor.description]  
    #     results_abs = []
    #     for row in cursor.fetchall():
    #         results_abs.append(dict(zip(columns, row)))
    #     cursor.nextset()  
    #     columns = [column[0] for column in cursor.description]  
    #     results_authors = []
    #     for row in cursor.fetchall():
    #         results_authors.append(dict(zip(columns, row)))
        
    #     return {'sessions': results_sess,'abstracts':results_abs,'authors':results_authors}

# Author: NANDHINI END-------------------


