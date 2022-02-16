from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,session
from core.model.Sessions import Sessions
from core.model.Poster import Poster
from core.model.User import UserModel 
from core.model.AuthorsModel import AuthorsModel
from urllib.parse import unquote

import datetime
from datetime import timedelta,date,datetime,time
from random import randint
import json,utils
from .. import current_app,cache,Cryptography
from core.library.route_group import RouteGroup


app = Blueprint('sessions', __name__)


#-------------------------- Sridhar  --------------------------#
# Live Screen


@app.route('/live_session', methods=['GET'])
# @cache.cached(timeout=50)
def live_session():
    s = Sessions()
    try:
        encrypted_user_id = request.args.get('user_id')
        print("live_session")
        print(encrypted_user_id)
        new_date = datetime.now().strftime('%Y-%m-%d')
        return session_halls(new_date)
    except Exception as e:
        return redirect (url_for('user.Login'))   
    # # print(new_date)
    # # get current date live
    # current_session =  s.getsessiondate(new_date)
    # # print(current_session);
    # if current_session:
    #     results  =  s.getSessionHalls(new_date)
    #     if len(results) > 0:
            
    #     else:
    #         return redirect(url_for('sessions.Programsheet'))
    # else:
    #    return redirect(url_for('sessions.Programsheet'))   
   
#Dates Screen
@app.route('/session_dates', methods=['GET'])
def session_dates():
    s = Sessions()
    # get current date live
    results  =  s.getSessionDates()

    return render_template('hall_screen/dates_screen.html',results=results)

#Hall Screen
@app.route('/session_halls/<s_date>', methods=['GET'])
# @cache.cached(timeout=50)
def session_halls(s_date):
    try:
        encrypted_user_id = request.args.get('user_id')
        user_id = Cryptography.decrypt(encrypted_user_id)   
        print("session_halls")
        print(encrypted_user_id)         
        if user_id:
            print("call hall")
            results = {}
            return render_template('hall_screen/halls_screen.html',results=results,s_date=s_date,encrypted_user_id=encrypted_user_id)    
        else :
            return redirect (url_for('user.Login'))        
    except Exception as e:
        return redirect (url_for('user.Login'))      

@app.route('/session/<s_date>/<s_hall>', methods=['GET'])
def session_by_date_hall(s_date,s_hall):
    try:
        encrypted_user_id = request.args.get('user_id')
        user_id = Cryptography.decrypt(encrypted_user_id)    
        print("session")
        print(encrypted_user_id)    
        print("s_date+s_hall")
        s = Sessions()
        session_result = s.getSessionDateHall(unquote(s_date),unquote(s_hall))
        if session_result:
            session_id = session_result[0].get('session_id')
        else:
            return redirect (url_for('user.Lobby'))
        
        if user_id:
            sa_id = 0
            # session_result = s.getSession(session_id)
            session_date_time=session_result[0].get('session_start_date_time')
            next_session = s.nextsession(session_date_time)
            return render_template('hall_screen/live_stream.html',results=session_result,session_id=session_id,sa_id=sa_id,next_session=next_session,s_date=s_date,s_hall=s_hall,user_id=user_id,encrypted_user_id=encrypted_user_id)
        else :
            print('No session login')
            return redirect (url_for('user.Login'))    
    except Exception as e:
        return redirect (url_for('user.Login'))            

#-------------------------- Sridhar --------------------------#



#----------------Balaji---------------------------#
#-----------Lounge--------------#
@app.route('/lounge', methods =["GET", "POST"])
def Lounge():
    return render_template('lounge/lounge.html')                        

@app.route('/lounge/helpdesk', methods =["GET", "POST"])
def Helpdesk():
    return render_template('lounge/helpdesk.html')

@app.route('/lounge/networkzone', methods =["GET", "POST"])
def Networkzone():
    return render_template('lounge/networkzone.html')

@app.route('/lounge/halls', methods =["GET", "POST"])
@app.route('/lounge/halls/<progdate>', methods =["GET", "POST"])
def Halls(progdate=None):
    s       =   Sessions()
    dates   =   s.get_dates()
    today   = date.today()
    if progdate is None:        
        progdates       =   s.get_progdates()
        progdate    =   progdates[0]
        for i in progdates:
            if i == today:
                progdate    =   i            
                
    halls   =   s.get_all_halls(progdate)
    
    return render_template('lounge/halls.html', dates=dates, halls=halls, progdate=progdate)


@app.route('/lounge/halls/<progdate>/<hall>', methods =["GET", "POST"])
def Halldata(progdate=None,hall=None):
    s                   =   Sessions()
    progdate            =   progdate
    searchtxt           =   ''
    searchhall          =   hall 
    
    today = date.today()
    # print('today:')
    # print(today)
    if progdate is None:
        progdates       =   s.get_progdates()
        progdate        =   progdates[0]
        for i in progdates:
            if i == today:
                progdate    =   i
            else:
                progdate    =   progdates[0]    
    
    data_xaxis          =   s.get_all_halls(progdate)
    data                =   s.get_data(progdate,searchtxt,searchhall)        
    message             =   data['message']
    session_data        =   data['Result']
    daystart            =   data['daystart']
    dayend              =   data['dayend']
    dictList            =   data['dictList']
    hall                =   data['hall']
    
    dates               =   s.get_dates()
    allhalldata =   {}    
    for i in data_xaxis:
        # print(i)
        starttime_list  =   s.get_hallstarttime(progdate, i)
        allhalldata[i]  =   starttime_list
    

    final_data  =   {} 
    if session_data:
        new_sessions = [dict(r) for r in session_data] if session_data else None
        for i in new_sessions: 
            # print(i)
            start_date_time     =   i['session_start_date_time']  #get start datetime
            end_date_time       =   i['session_end_date_time']    #get end datetime
            start_time          =   start_date_time.time().strftime('%H:%M') #convert start datetime to time format
            end_time            =   end_date_time.time().strftime('%H:%M')   #convert end datetime to time format  
            Session_duration    =   i['session_hall'] + "-" + start_time
                    
            final_data[Session_duration]    =   i
    
    return render_template('programsheet/programsheet.html',  
                    progdate    =   progdate, 
                    allhalldata =   allhalldata,
                    daystart    =   daystart, 
                    dayend      =   dayend, 
                    dictList    =   dictList, 
                    final_data  =   final_data, 
                    dates       =   dates,
                    hall        =   hall,
                    data_xaxis  =   data_xaxis,                    
                    searchtxt   =   searchtxt,
                    searchhall  =   searchhall,
                    message     =   message)
    


#-----------Programsheet--------------#
# displaying the program sheet info..
@app.route('/programsheet/', methods =["GET", "POST"])
@app.route('/programsheet/<progdate>', methods =["GET", "POST"])
def Programsheet(progdate=None):    
    try:
        searchtxt           =   ''
        searchhall          =   ''
        progdate            =   progdate    
        

        
        # get search value from form
        if request.method   == 'POST':
            search          =   request.form["searchtxt"]    
            searchtxt       =   "%{}%".format(search)
            searchhall      =   str((request.form["searchhall"]))
            # print("searchhall")
            # print(searchhall)
            # print("searchtxt")
            # print(searchtxt)        
        
        s   =   Sessions()
        new_sessions        =   []
        
        # set default progdate as first day of the conference
        today = date.today()
        # print('today:')
        # print(today)
        if progdate is None:
            progdates       =   s.get_progdates()
            progdate        =   progdates[0]
            for i in progdates:
                if i == today:
                    progdate    =   i
            title_date          =   datetime.strftime(progdate,'%d-%b-%Y')         
        else:
            title_date  =   datetime.strptime(progdate,'%Y-%m-%d').strftime('%d-%b-%Y')

        # print(">>progdate<<")
        # print(progdate)
        dates               =   s.get_dates()
        data_xaxis          =   s.get_all_halls(progdate)   # we are not using this variable as we are using hall variable for x axis but still we use this for allhalldata
        data                =   s.get_data(progdate,searchtxt,searchhall)  # passing search parameters from form              
        message             =   data['message']
        session_data        =   data['Result']
        daystart            =   data['daystart']
        dayend              =   data['dayend']
        dictList            =   data['dictList']
        hall                =   data['hall']
        
        
        # get starttime for all halls
        allhalldata =   {}    
        for i in data_xaxis:
            # print(i)
            starttime_list  =   s.get_hallstarttime(progdate, i)
            allhalldata[i]  =   starttime_list
        # print('allhalldata')
        # print(allhalldata[i][1])
        # print(">>allhalldata<<")
        # print(allhalldata)

        final_data  =   {} 
        if session_data:
            new_sessions = [dict(r) for r in session_data] if session_data else None
            for i in new_sessions: 
                # print(i)
                start_date_time     =   i['session_start_date_time']  #get start datetime
                end_date_time       =   i['session_end_date_time']    #get end datetime
                start_time          =   start_date_time.time().strftime('%H:%M') #convert start datetime to time format
                end_time            =   end_date_time.time().strftime('%H:%M')   #convert end datetime to time format  
                Session_duration    =   i['session_hall'] + "-" + start_time
                        
                final_data[Session_duration]    =   i
        # print(">>final_data<<")
        # print(final_data)
    
        return render_template('programsheet/programsheet.html', 
                        progdate    =   progdate, 
                        allhalldata =   allhalldata,
                        daystart    =   daystart, 
                        dayend      =   dayend, 
                        dictList    =   dictList, 
                        final_data  =   final_data, 
                        dates       =   dates,
                        hall        =   hall,
                        data_xaxis  =   data_xaxis,                    
                        searchtxt   =   searchtxt,
                        searchhall  =   searchhall,
                        message     =   message,
                        title_date  =   title_date)
    except Exception as e:
        current_app.logger.error(str(e))
    

#-----------Active Sessions--------------#

@app.route('/activesessions', methods =["GET", "POST"])
def Activesessions():    
    searchtxt           =   ''
    searchhall          =   ''
    today               =   date.today()    
    
    
    # get search value from form
    if request.method   == 'POST':
        search          =   request.form["searchtxt"]    
        searchtxt       =   "%{}%".format(search)
        searchhall      =   str((request.form["searchhall"]))        
    

    s   =   Sessions()
    new_sessions        =   []
    
    # check if today is among progdates -- if no data, send Mess else process using today as progdate
    datum               =   s.checkdate(today)    
    if not datum:
        Mess            =   'No Active Sessions today.'
        return render_template('programsheet/activesessions.html', Mess=Mess)
    else:
        # set default progdate as first day of the conference        
        progdate            =   today
        data_xaxis          =   s.get_all_halls(progdate)   # we are not using this variable as we are using hall variable for x axis but still we use this for allhalldata
        data                =   s.get_activesessions_data(progdate,searchtxt,searchhall)  # passing search parameters from form              
        Message             =   data['Message']
        if Message:
            return render_template('programsheet/activesessions.html', progdate=progdate, data_xaxis=data_xaxis, Message=data['Message'])    
        else:
            session_data    =   data['Result']
            daystart        =   data['daystart']
            dayend          =   data['dayend']
            dictList        =   data['dictList']
            dates           =   data['dates']
            hall            =   data['hall']
        
        new_sessions = [dict(r) for r in session_data] if session_data else None
        
        
        # get starttime for all halls
        allhalldata =   {}    
        for i in data_xaxis:
            # print(i)
            starttime_list  =   s.get_hallstarttime(progdate, i)
            allhalldata[i]  =   starttime_list
        # print('allhalldata')
        # print(allhalldata[i][1])
        

        final_data  =   {} 
        for i in new_sessions: 
            # print(i)
            start_date_time     =   i['session_start_date_time']  #get start datetime
            end_date_time       =   i['session_end_date_time']    #get end datetime
            start_time          =   start_date_time.time().strftime('%H:%M') #convert start datetime to time format
            end_time            =   end_date_time.time().strftime('%H:%M')   #convert end datetime to time format  
            Session_duration    =   i['session_hall'] + "-" + start_time
                    
            final_data[Session_duration]    =   i
        
        return render_template('programsheet/activesessions.html', 
                        progdate    =   progdate, 
                        allhalldata =   allhalldata,
                        daystart    =   daystart, 
                        dayend      =   dayend, 
                        dictList    =   dictList, 
                        final_data  =   final_data, 
                        dates       =   dates,
                        hall        =   hall,
                        data_xaxis  =   data_xaxis,                    
                        searchtxt   =   searchtxt,
                        searchhall  =   searchhall)


#---------------Author: Balaji end-----------------------------#

#---------------Author: Nandhini start-------------------------

@app.route('/hall_screen', methods =["GET", "POST"])
@app.route('/hall_screen/<int:session_id>',methods =["GET", "POST"])
def hall_screen(session_id=None):
    u = UserModel()
    user = u.Auth()
    if user:
        s = Sessions()
        current_session = None
        previous_sessions = None
        upcoming_sessions = None
        dt = datetime.now()
        if session_id :
            current_session = s.getSessionId(session_id)
            # print('current_session___')
            # print(current_session)
        else :
            current_session = s.getCurrentSession()

        if current_session:
            dt =  current_session['session_end_date_time']

        previous_upcoming_session = s.previous_upcoming_session(dt)
        previous_sessions = previous_upcoming_session['previous_ses']
        upcoming_sessions = previous_upcoming_session['upcoming_ses']
        return render_template('hall_screen/hall_screen.html',session_id=session_id,current_session=current_session,previous_sessions=previous_sessions,upcoming_sessions=upcoming_sessions)
    else :
        print('No session login')
        return redirect (url_for('user.Login'))

@app.route('/test', methods = ["GET"])
def test():
    user_id = session.get('user')
    #print("helllooo user_id")
    # print(user_id)
    return user_id


@app.route('/sessions', methods = ["GET"])
def get_session():
    s = Sessions()
    results = s.getallsession() 
    # print(results)
    # return "test"
    return render_template('hall_screen/sessions.html',ses_results=results)

@app.route('/session/<s_date>', methods=['GET'])
def session_by_date(s_date):
    s = Sessions()
    session_result = s.getsessiondate(s_date)
    session_id = session_result[0].get('session_id')
    print('session_id')
    print(session_id)
    # session_date = get_session_date.get('date')
    # get_session_date = 
    # session_id = 1
    u = UserModel()
    user = u.Auth()
    if user:
        sa_id = 0
        # print('user_id')
        # print(user.get('user_id'))
        # data = {
        #         'user_id' :user.get('user_id'),
        #         'session_id' :session_id ,
        #         'entry_time' :datetime.now(),
        #         'created_at': datetime.now(),

        #     }
        # session_attendance = s.session_attendance(data)
        # get_s_att_id = s.get_s_att(session_id)
        # sa={}
        # for a in get_s_att_id['session_att']:
        #     sa_id = a['sa_id']
        
        # session_result = s.getSession(session_id)
        session_date_time=session_result[0].get('session_start_date_time')
        next_session = s.nextsession(session_date_time)
        # print('next_session')
        # print(next_session)
        return render_template('hall_screen/program_live_pages.html',results=session_result,session_id=session_id,sa_id=sa_id,next_session=next_session,s_date=s_date)
    else :
        print('No session login')
        return redirect (url_for('user.Login'))






@app.route('/session/<int:session_id>', methods=['GET'])
def get_session_by_id(session_id):
    s = Sessions()
    u = UserModel()
    user = u.Auth()
    if user:
        sa_id = 0
        # print('user_id')
        # print(user.get('user_id'))
        # data = {
        #         'user_id' :user.get('user_id'),
        #         'session_id' :session_id ,
        #         'entry_time' :datetime.now(),
        #         'created_at': datetime.now(),

        #     }
        # session_attendance = s.session_attendance(data)
        # get_s_att_id = s.get_s_att(session_id)
        # sa={}
        # for a in get_s_att_id['session_att']:
        #     sa_id = a['sa_id']
        
        session_result = s.getSession(session_id)
        session_date_time=session_result[0].get('session_start_date_time')
        next_session = s.nextsession(session_date_time)
        # print('next_session')
        # print(next_session)
        return render_template('hall_screen/program_live_pages.html',results=session_result,session_id=session_id,sa_id=sa_id,next_session=next_session)
    else :
        print('No session login')
        return redirect (url_for('user.Login'))

# @app.route('/get_all_ads_banner', methods=['POST'])        
# @cache.cached(timeout=7200)
# def get_all_ads_banner():
#     # print(session_id)
#     s = Sessions()
#     get_all_banner_image = s.getallbanner()
#     banner_count = len(get_all_banner_image)
    
#     print(banner_count[0].get("count"))
#     if banner_count:
#         get_banner_count = banner_count[0].get("count")
#     # print('get_banner_image')
#     # print(get_banner_image)
    
#     if get_banner_image:
#         return jsonify({'data':get_banner_image[0],'count':get_banner_count} )
#     else :
#         return jsonify({'data':None,'count':get_banner_count})



@app.route('/get_ads_banner', methods=['POST'])
@cache.cached(timeout=7200)
def get_ads_banner():
    # print(session_id)
    banner_id = request.values['banner_id']
    session_id = request.values['session_id']
    s = Sessions()
    get_banner_image = s.getbanner(banner_id,session_id)
    banner_count = s.getbannercount(session_id)
    print("banner_count")
    print(banner_count[0].get("count"))
    if banner_count:
        get_banner_count = banner_count[0].get("count")
    # print('get_banner_image')
    # print(get_banner_image)
    
    if get_banner_image:
        return jsonify({'data':get_banner_image[0],'count':get_banner_count} )
    else :
        return jsonify({'data':None,'count':get_banner_count})
        

@app.route('/close_time/<int:session_id>/<int:user_id>', methods=['GET','POST'])
def closetime(session_id,user_id):
    # print(session_id)
    u = UserModel()
    user = u.Auth()
    user_id = user.get('user_id')   
    # print(user_id)
    data = {
            'close_time' :datetime.now(),
            'updated_at': datetime.now(),
        }
    s = Sessions()
    data = s.session_close_time(data,session_id,user_id)
    # print('session_close_time')
    # print(session_close_time)
    return jsonify({'status':1}) 

                       
@app.route('/get_debate/<int:session_id>', methods=['GET','POST'])
def getdebate(session_id):
    u = UserModel()
    user = u.Auth()
    # user_id = user.get('user_id') 
    # answer   = request.form['user_option']  
    s = Sessions()
    option_debates = s.get_debate(session_id)
    html =  render_template('hall_screen/option_debate.html',option_debates=option_debates)
    return jsonify({'status':1,'html':html})


@app.route('/save_option/<int:session_id>', methods=['GET','POST'])
def saveoption(session_id):
    u = UserModel()
    user = u.Auth()
    user_id = user.get('user_id') 
    data = {
            'user_id' : user_id,
            'session_id' : session_id ,
            'd_option_id' :request.form['option_id'],
            'created_at': datetime.now(),
        }
    s = Sessions()
    user_answer = s.user_answer(data)
    return jsonify({'status':1,'msg':'Your option is submitted successfully'})


# @app.route('/get_header_title/<s_date>', methods=['GET','POST'])
# def get_header_title(s_date):
#     s = Sessions()
#     results = s.getCurrentSession_by_date(s_date)
#     # if results == None:
#     #     results = s.getSessionId(1)
#     # print('results')
#     # print(results)
#     new_date = datetime.strptime(s_date,'%Y-%m-%d').strftime('%d-%b-%Y')
#     html =  render_template('hall_screen/session_header.html',s=results,s_date=new_date)
#     return jsonify({'status':1,'html':html,'s_date':new_date})  

@app.route('/get_header_title/<s_date>/<s_hall>', methods=['GET','POST'])
@cache.cached(timeout=7200)
def get_header_title(s_date,s_hall):
    s = Sessions()
    s_date = unquote(s_date)
    s_hall = unquote(s_hall)
    results = s.getCurrentSession_by_date_hall(s_date,s_hall)
    stream = "";
    if results:
        stream = results.get('live_stream')
        session_id = results.get('session_id')
    else:
        session_result = s.getSessionDateHall(s_date,s_hall)
        session_id = session_result[0].get('session_id')
    
    print("get_header_title")
    new_date = datetime.strptime(s_date,'%Y-%m-%d').strftime('%d-%b-%Y')
    html =  render_template('hall_screen/session_header.html',s=results,s_date=new_date,s_hall=s_hall)
    return jsonify({'status':1,'html':html,'s_date':new_date,'session_id':session_id,'stream':stream})  



# Get two date data
# @app.route('/session', methods = ["GET","POST"])
# def session():
#     s = Sessions()
#     results = s.getpreupcomsession() 
#     print('test')
#     print(results) 
#     return render_template('hall_screen/previous_upcom_session.html',results=results)


@app.route('/backoffice/authors/<int:session_id>', methods = ["GET"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def Authors(session_id):
    if request.method == "GET":
        
        # if session.get('user'):
            user_id = session.get('user')
            roles = AuthorsModel().getRoles()

            selected_authors_list = AuthorsModel().getSeletedAuthorsForSession(session_id)
            if selected_authors_list:
                data = [dict(r) for r in selected_authors_list]
                authors_data_json = json.dumps(data)
            return render_template('backoffice/add_user_for_sessions.html', user_id = user_id ,session_id = session_id,roles = roles,authors_data_json = authors_data_json)
        # else:
        #     return render_template('backoffice/bo_login.html')

@app.route('/backoffice/get_authors', methods = ["POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def GetAuthors():
    # user_id      = session.get('user')
    search_input = request.form['search_input']
    authors_data = AuthorsModel().getAuthorsData(search_input)

    if authors_data:
        for index, value in enumerate(authors_data):
            created_at    = value['created_at']
            last_login    = value['last_login']
            if created_at:
                dt_string = created_at.strftime("%Y-%m-%d %H:%M:%S")
                value['created_at']   = dt_string
            if last_login:
                dt_string_2 = last_login.strftime("%Y-%m-%d %H:%M:%S")
                value['last_login']   = dt_string_2
        
        authors_data_json = json.dumps(authors_data)
        # js = json.dumps()

        return authors_data_json
    else :
        return "" 
    


# get_selected_authors
@app.route('/backoffice/get_user', methods = ["POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def GetUser():
    if request.method == "POST":
        # user_id      = session.get('user')
        selected_user_id = request.form['selected_user_id']
        authors_data = UserModel().getuser(selected_user_id)

        if authors_data:
            data = [dict(r) for r in authors_data]
            
            for index, value in enumerate(data):
                created_at    = value['created_at']
                last_login    = value['last_login']
                if created_at:
                    dt_string = created_at.strftime("%Y-%m-%d %H:%M:%S")
                    value['created_at']   = dt_string
                if last_login:
                    dt_string_2 = last_login.strftime("%Y-%m-%d %H:%M:%S")
                    value['last_login']   = dt_string_2

            
            authors_data_json = json.dumps(data) 
            return authors_data_json 
        else :
            return ""    


@app.route('/backoffice/get_author', methods = ["POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def GetAuthor():
    if request.method == "POST":
        # user_id      = session.get('user')
        author_id = request.form['author_id']
        data = AuthorsModel().getAuthor(author_id)
        return jsonify(data)
    else :
        return ""    
# save_selected_authors    

@app.route('/backoffice/save_selected_authors', methods = ["POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def SaveSelectedAuthors():
    if request.method == "POST":
        # print("In save authors function")
        user_id    = request.form['user_id'] or None
        session_id = request.form['session_id'] or None
        role_id    = request.form['role_id'] or None

        name       = request.form['name'] or None
        email      = request.form['email'] or None
        mobile     = request.form['mobile'] or None

        topics   = request.form['topics'] or None

        duration   = request.form['duration'] or None


        author_id   = request.form['author_id'] or None

        data  = {"user_id" :user_id,
        "session_id" : session_id,
        "role_id" : role_id,
        "name" : name,
        "email" : email,
        "mobile" : mobile,
        "topic" : topics,
        "duration" : duration}

        author_id = int(author_id)
        if author_id > 0:
            # print("In controller update block")
            update_data = AuthorsModel().UpdateSelectedAuthors(author_id,data)    
        else :
            
            # print("In controller save block")
            authors_data = AuthorsModel().insert_authors(data)
            


        # authors_data = AuthorsModel().insert_authors(data)
        msg = "success"
        selected_authors_list = AuthorsModel().getSeletedAuthorsForSession(session_id)
        if selected_authors_list:
            
            data = [dict(r) for r in selected_authors_list]
            authors_data_json = json.dumps(data)


        return authors_data_json

        # if authors_data:
        #     data = [dict(r) for r in authors_data]
            
        #     for index, value in enumerate(data):
        #         created_at    = value['created_at']
        #         last_login    = value['last_login']
        #         if created_at:
        #             dt_string = created_at.strftime("%Y-%m-%d %H:%M:%S")
        #             value['created_at']   = dt_string
        #         if last_login:
        #             dt_string_2 = last_login.strftime("%Y-%m-%d %H:%M:%S")
        #             value['last_login']   = dt_string_2

            
        #     authors_data_json = json.dumps(data) 
        #     return authors_data_json 
        # else :
        #     return None              

# remove_selected_authors
@app.route('/backoffice/remove_selected_authors', methods = ["POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def RemoveSelectedAuthors():
    if request.method == "POST":
        author_id    = request.form['author_id']
        session_id = request.form['session_id']
        remove_authors        = AuthorsModel().delete_authors(author_id)
        selected_authors_list = AuthorsModel().getSeletedAuthorsForSession(session_id)
        if selected_authors_list:
            
            data = [dict(r) for r in selected_authors_list]
            authors_data_json = json.dumps(data)


        return authors_data_json

# edit_selected_authors   
@app.route('/backoffice/edit_selected_authors', methods = ["POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def EditSelectedAuthors():
    if request.method == "POST":
        user_id    = request.form['selected_user_id'] or None
        session_id = request.form['session_id'] or None

        selected_authors_list = AuthorsModel().EditAuthorsForSession(user_id,session_id)
        if selected_authors_list:
            
            data = [dict(r) for r in selected_authors_list]
            authors_data_json = json.dumps(data)
            # print(authors_data_json)
            # print(type(authors_data_json))
            return authors_data_json
        else :
            msg = "No data found"
            return json.dumps(msg)         


        