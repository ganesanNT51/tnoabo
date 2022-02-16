from flask import request, Blueprint, jsonify, redirect, url_for,flash, render_template
from core.model.BOModel import BOModel
from core.model.User import UserModel
from core.model.Halls import Halls
from core.model.Sessions import Sessions
from random import randint
import datetime
from datetime import timedelta,date,datetime
import requests, mandrill, json
from .. import Helper,Cryptography
from datetime import timedelta
from flask import session, app
from core.library.route_group import RouteGroup
import pytz
from core.library.sms import SMS
from core.library.email import EMAIL
# import collections
from werkzeug.useragents import UserAgent
from urllib.parse import unquote

app = Blueprint('backoffice', __name__)

UTC = pytz.utc
IST = pytz.timezone('Asia/Calcutta')
datetime_ist = datetime.now(IST)


@app.route('/set/<value>', methods = ["GET", "POST"])
def set_session(value):
    session['value'] = value
    return f'seted value is : {value}'


@app.route('/get', methods = ["GET", "POST"])
def get_session():
    return f'the value from session : { session.get("value")}' 

@app.route('/' , methods = ["GET"])
def BOLogin():
    print('ín form')
    return render_template('backoffice/bo_login.html')

@app.route('/boindex', methods = ["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def BOIndex():
    if request.method == "GET":
        status = 1
        if session.get('backoffice'):
            user = session.get('backoffice')
            # print('in session')
            bo_user_id = request.args.get('bo_user_id')
            encrypted_user_id= Cryptography.encrypt(bo_user_id)
            boModel = BOModel()
            output = boModel.get_registered_data()
            registered_delegate_count = boModel.get_registered_count()
            reg_count = registered_delegate_count['reg_count']
            # print("Registered count")
            # print(registered_delegate_count['reg_count'])
            return render_template('backoffice/registration_index.html', user = user ,bo_user_id=encrypted_user_id,reg_data= output,reg_delegate_count = reg_count)
        else:
            print('in main page')
            return render_template('backoffice/bo_login.html')

@app.route('bo_logout', methods = ["GET", "POST"])
def BOLogout():
    session.pop('backoffice')
    session.pop('_flashes', None)
    return redirect(url_for('backoffice.BOLogin'))            


# PostBOLogin   

@app.route('/backoffice' , methods = ["POST"])
def PostBOLogin():
    if request.method == "POST":
        form_email = request.form['email']
        form_password = request.form['password']
        if  not form_email  or not form_password:
            flash('Please enter username and password')
            return redirect (url_for('backoffice.BOLogin'))
        else :
            boModel = BOModel()
            user_output = boModel.get_users_email_data(form_email,form_password)
            if user_output : 
                # print("form input password " + form_password)
                db_pass =  user_output['password']
                # print("user name " + user_output['user_name'])
                # print(" db password " + db_pass )
                if form_password == db_pass:
                    if user_output['is_active'] == 1:
                        print(user_output['password'] + "and given password is " + form_password )
                        bo_user_id = user_output['bo_user_id']
                        print(  bo_user_id )
                        print(datetime.now())

                        boModel.update_last_login(bo_user_id,datetime.now());
                        
                        
                        session['backoffice'] =  user_output
                        encrypted_bo_user_id= Cryptography.encrypt(bo_user_id)
                        print(encrypted_bo_user_id)
                        return redirect (url_for('backoffice.BOIndex',bo_user_id= encrypted_bo_user_id))
                    else :
                        flash('Permission denied.' )
                        return redirect (url_for('backoffice.BOLogin'))
                     
                else : 
                    status = 0
                    flash('Passsword invalid. Please check the password.  ' )
                    return redirect (url_for('backoffice.BOLogin'))

            else:
                status = 0
                msg = "Username is not registered."

            flash("Username is not registered." )
            return redirect (url_for('backoffice.BOLogin'))   



#---------------Author: Balaji start-------------------------#

#-----------Backoffice Start--------------#
@app.route('/backoffice/delete/<id>', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def Delete(id=None):
    # try:
    id                  =   id
    s                   =   Sessions()    
    delete_session      =   s.delete_session(id)
    # except Exception as e:
    #     current_app.logger.error(str(e))
    return redirect(url_for('backoffice.SessionIndex'))

# Updated by Balaji 2021-05-08 10:38 AM
# Update by sridhar 2021-05-05 12:39 PM
@app.route('/backoffice/edit/<id>', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def SessionEdit(id=None):
    # try:        
	h 					= 	Halls()
	id                  =   id          
	s                   =   Sessions()
	results             =   s.getSession(id)
	result 				=   results[0]
	#print(result)
	halls               =   h.get_halls()
	start_date          =   ''
	end_date            =   ''
	start_time          =   ''
	end_time            =   ''
	message             =   ''

			
	start_date_time     =   result['session_start_date_time']  #get start datetime
	end_date_time       =   result['session_end_date_time']    #get end datetime
	start_time          =   start_date_time.time().strftime('%H:%M') #convert start datetime to time format
	end_time            =   end_date_time.time().strftime('%H:%M')   #convert end datetime to time format  
	start_date          =   datetime.strftime(start_date_time, '%Y-%m-%d')
	end_date            =   datetime.strftime(end_date_time, '%Y-%m-%d')
	session_hall        =   result['session_hall']
	

	if request.method   == 'POST':
		session_start_date_time =   ''
		session_end_date_time   =   ''
		from_date               =   request.form["from_date"]
		to_date                 =   request.form["to_date"]
		start_time              =   request.form["start_time"]
		end_time                =   request.form["end_time"]

		
		data = {                    
			'session_hall'              :   request.form["searchhall"],
			'date'                      :   from_date,
			'session_start_date_time'   :   from_date +" "+ start_time,
			'session_end_date_time'     :   to_date +" "+ end_time,
			'session_title'             :   request.form["session_title"],
			'session_subtitle'          :   request.form["session_subtitle"],
			'session_desc'              :   request.form["session_desc"],
			'video_link'                :   request.form["video_link"],
			'bg_color'                  :   request.form["bg_color"],
			'zoom_link'         		:   request.form["zoom_link"],
			'live_stream'         		:   request.form["live_stream"],
			'zoom_meeting_id'          	:   request.form["zoom_meeting_id"],
			'zoom_password'       		:   request.form["zoom_password"]				
			}

		# print(data)

		#string to datetime conversion
		# print('conversions')
		from_date               =   datetime.strptime(from_date, '%Y-%m-%d')            
		# print(from_date)
		to_date                 =   datetime.strptime(to_date, '%Y-%m-%d')
		# print(to_date)
		# start_time              =   datetime.strptime(start_time, '%H:%M')
		# print(start_time)
		# end_time                =   datetime.strptime(end_time, '%H:%M')
		# print(end_time)
		# if (from_date <= to_date):
		#     print("from_date is Greater")
		# if (datetime.strptime(start_time, '%H:%M') < datetime.strptime(end_time, '%H:%M')):
		#     print("start_time is Greater")

		if (from_date <= to_date and datetime.strptime(start_time, '%H:%M') < datetime.strptime(end_time, '%H:%M') or from_date <= to_date and datetime.strptime(start_time, '%H:%M') > datetime.strptime(end_time, '%H:%M')):
			update_session      =   s.update_session(data, id)
			start_date          =   request.form["from_date"]
			end_date            =   request.form["to_date"]
			start_time          =   request.form["start_time"]
			end_time            =   request.form["end_time"]
			session_title       =   request.form["session_title"]
			session_desc        =   request.form["session_desc"]
			session_subtitle    =   request.form["session_subtitle"]
			video_link          =   request.form["video_link"]
			bg_color            =   request.form["bg_color"]
			zoom_link          	=   request.form["zoom_link"]
			live_stream         =   request.form["live_stream"]
			zoom_meeting_id     =   request.form["zoom_meeting_id"]
			zoom_password       =   request.form["zoom_password"]
			halls               =   s.get_halls()
			message             =   "Session has been updated successfully!"

			result              =   {'searchhall': request.form["searchhall"],'start_date': request.form["from_date"], 'end_date': request.form["to_date"], 
									'start_time': request.form["start_time"], 'end_time': request.form["end_time"],
									'session_title': request.form["session_title"], 'session_desc': request.form["session_desc"], 
									'session_subtitle': request.form["session_subtitle"], 'video_link': request.form["video_link"], 'bg_color': request.form["bg_color"],
									'zoom_link' : request.form["zoom_link"], 'live_stream': request.form["live_stream"],
									'zoom_meeting_id' : request.form["zoom_meeting_id"],'zoom_password' : request.form["zoom_password"]}        
		else:
			print('failed if condition')
			message             =   "Start date and start time cannot be greater than end date and end time."
	
	# except Exception as e:
	#     current_app.logger.error(str(e))
	return render_template('backoffice/editsession.html', halls=halls, result=result, start_time=start_time, end_time=end_time,start_date=start_date, end_date=end_date,session_hall=session_hall,message=message,id=id)


@app.route('/backoffice/addsessions', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def CreateSession():
    # try:
	h 				= Halls()
	result 	 		=   {}
	message         =   ''
	session_hall    =   ''
	if request.method   == 'GET':
		halls = h.get_halls()
		# halls = [chr(x) for x in range(ord('A'), ord('Z') + 1)] 
		return render_template('backoffice/createsession.html', halls=halls)

	result              =   {}
	if request.method   == 'POST':
		session_start_date_time =   ''
		session_end_date_time   =   ''
		message                 =   ''
		halls = h.get_halls()

		from_date               =   request.form["from_date"]
		to_date                 =   request.form["to_date"]
		start_time              =   request.form["start_time"]
		end_time                =   request.form["end_time"]
		

		data = {                    
					'session_hall'              :   request.form["searchhall"],
					'date'                      :   from_date,
					'session_start_date_time'   :   from_date +" "+ start_time,
					'session_end_date_time'     :   to_date +" "+ end_time,
					'session_title'             :   request.form["session_title"],
					'session_subtitle'          :   request.form["sub_title"],
					'session_desc'              :   request.form["session_desc"],
					'video_link'                :   request.form["video_link"],
					'bg_color'                  :   request.form["bg_color"],
					'zoom_link'         		:   request.form["zoom_link"],
					'live_stream'         		:   request.form["live_stream"],
					'zoom_meeting_id'          	:   request.form["zoom_meeting_id"],
					'zoom_password'       		:   request.form["zoom_password"]
					
				}

		#string to datetime conversion
		# print('conversions')
		from_date               =   datetime.strptime(from_date, '%Y-%m-%d')            
		# print(from_date)
		to_date                 =   datetime.strptime(to_date, '%Y-%m-%d')
		# print(to_date)
		# print(data)
		
		if (from_date <= to_date and datetime.strptime(start_time, '%H:%M') < datetime.strptime(end_time, '%H:%M')):
			s                   =   Sessions()    
			insert_session      =   s.insert_session(data)
			message             =   "Session created succesfully!"        
			# print(message)                
		elif(from_date <= to_date and datetime.strptime(start_time, '%H:%M') > datetime.strptime(end_time, '%H:%M')):
			s                   =   Sessions()    
			insert_session      =   s.insert_session(data)
			message             =   "Session created succesfully!"        
			# print(message)                
		else:
			# print('failed if condition')
			message             =   "Start date and start time cannot be greater than end date and end time."
			result              =   {'start_date': request.form["from_date"], 'end_date': request.form["to_date"], 
									'start_time': request.form["start_time"], 'end_time': request.form["end_time"],
									'session_title': request.form["session_title"], 'session_desc': request.form["session_desc"], 
									'session_subtitle': request.form["sub_title"], 'video_link': request.form["video_link"], 'bg_color': request.form["bg_color"],
									'zoom_link' : request.form["zoom_link"], 'live_stream': request.form["live_stream"],
									'zoom_meeting_id' : request.form["zoom_meeting_id"],'zoom_password' : request.form["zoom_password"]}

    # except Exception as e:
    #     current_app.logger.error(str(e))
	
	return render_template('backoffice/createsession.html',message=message, halls=halls, result=result)    
    

@app.route('/backoffice/sessionindex', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def SessionIndex():
    try:    
        s       =   Sessions()
        progdate            =   ''
        searchtxt           =   ''
        searchhall          =   ''
        message             =   ''
        session_data        =   []        
        
        data                =   s.fetchallsession(progdate,searchtxt,searchhall)        
        session_data        =   data['Result']

        if request.method   == 'POST':
            progdate        =   request.form["searchdate"]
            searchhall      =   request.form["searchhall"]
            search          =   request.form["searchtxt"]    
            searchtxt       =   "%{}%".format(search)

            data            =   s.fetchallsession(progdate,searchtxt,searchhall)    
            message         =   data['message']
            session_data    =   data['Result']
            halls           =   s.get_halls()
            dates           =   s.get_dates()
            # print("Inside post")
            # print(halls)
        
    except Exception as e:
        current_app.logger.error(str(e))
    message             =   message
    halls               =   s.get_halls()
    dates               =   s.get_dates()
    return render_template('backoffice/sessionindex.html',session_data=session_data,message=message,halls=halls,dates=dates)




# ---------------------- Sridhar commitment  ---------------------- #


@app.route('/backoffice/commitment_list', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def commitment_list():
    data    = UserModel().get_commitment_list()        
    # print(data)
    return render_template('backoffice/commitment_list.html',data=data)



@app.route('/backoffice/view_user_commitment/<int:user_id>', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def view_user_commitment(user_id):
    user    = UserModel().getuser(user_id)
    # print("user")
    # print(user[0])
    data    = UserModel().get_user_commitment(user_id)        
    # print(data)
    return render_template('backoffice/commitment_user_view.html',data=data,user=user)



@app.route('/backoffice/email_user_commitments' , methods = ["GET"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def email_user_commitments():
    user_ids = None
    users_db = UserModel().get_commitment_users_email(user_ids)
    # return jsonify(users_db)
    # return str(len(users_db))
    users = []
    append_list = []
    data = {}
    user_id = 0
    idx = 0
    print(len(users_db))
    # return str(len(users_db))
    for user in users_db:
        idx += 1
        print(idx)
        users.append(user.get("user_id"))
        if user_id == 0:
            append_list.append(user)
            user_id = user.get("user_id")
            print("user_id is 0")
            print(user_id)
        elif user_id == user.get("user_id"):
            append_list.append(user)
            print("user_id is =")
            print(user_id)
        if user_id != user.get("user_id"):
            if user_id>0:
                print("user_id is !=")
                print(user_id)
                data[str(user_id)] = append_list
                user_id = user.get("user_id")
                append_list = []
                append_list.append(user)
        if idx == len(users_db):
            data[str(user_id)] = append_list

        # print(data)        
        
    
    # print(list(dict.fromkeys(users)))
    for user in list(dict.fromkeys(users)):
        print(user)
        d = data.get(str(user));
        u = d[0]
        # email = "sai@numerotec.com"
        email = u.get("email")
        name  = (u.get("prefix") if u.get("prefix") else '')  + " " + (u.get("full_name") if u.get("full_name") else '')
        subject = name + " - Your Final Commitments for BOA 2021 Day 4"
        html = render_template('backoffice/email/commitment_mail.html',data=d,user=u)    
        print(email)
        EMAIL.sendMail(subject,html,email)
        
    return "success"

# ---------------------- commitment  End ---------------------- #



# *********************** GANESAN SESSION Spot Editer Forms  ********************#

@app.route('/backoffice/session_control', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def SessionControl():
    get_halls = BOModel().get_halls()
    # get_session_date
    get_session_date = BOModel().get_session_date()
    return render_template('backoffice/session_update_screen.html' ,halls = get_halls,session_date = get_session_date) 


@app.route('/backoffice/getsessions', methods =["GET", "POST"])
def Getsessions():

    hall_search  = request.args.get('hall_search') or None
    date_search = request.args.get('date_search')  or None

    # allsessions = Sessions().getallsession(hall_search,date_search)
    allsessions = BOModel().sessionFilter(hall_search,date_search)
    # sessionFilter
    current_dt_str = datetime_ist.strftime('%Y-%m-%d %H:%M:%S')
    current_dt = datetime. strptime(current_dt_str, '%Y-%m-%d %H:%M:%S')
    # print(current_dt)
    html =  render_template('backoffice/session_control_table.html',allsessions=allsessions,current_dt =current_dt,type=type)
    return jsonify({'message': "success",'status' : 1,'html':html}) 



# update_session    
@app.route('/backoffice/update_session', methods =["GET", "POST"])
@RouteGroup.bo_login_required #check if login else automatically redirect to login page
def UpdateSession():
    session_id    = request.form['session_id'] 
    session_title = request.form['session_title']
    # session_desc  = request.form['session_desc'] or None
    session_desc  = request.form['session_desc'] 
    video_link  = request.form['video_link'] 

    session_start_date_time = request.form['session_start_date_time']
    session_end_date_time   = request.form['session_end_date_time']

    dt_string = datetime_ist.strftime('%Y-%m-%d %H:%M:%S')
    # session_desc change into session_subtitle 

    data  = {"session_id" :session_id,
        "session_title" : session_title,
        "session_subtitle" : session_desc,
        "session_start_date_time" : session_start_date_time,
        "session_end_date_time" : session_end_date_time,
        "live_stream" : live_stream,
        "updated_at" : dt_string
    }

    update_session = Sessions().update_session(data, session_id)
    # print(update_session)
    allsessions = Sessions().getallsession()
    html =  render_template('backoffice/session_control_table.html',allsessions=allsessions)
    return jsonify({'message': "success",'status' : 1,'html':html}) 


    # *********************** GANESAN SESSION Spot Editer Forms  END ********************#
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    user_agent = UserAgent(request.headers.get('User-Agent'))
    os_name = user_agent.platform
    browser_name = user_agent.browser
    return jsonify({'ip_address': request.remote_addr, 'os_name':os_name,'browser_name' : browser_name})   
    
@app.route("/get_my_browser", methods=["GET"])
def get_my_browser():
    browser_info = request.headers.get('User-Agent') 
    return browser_info    
    
    


#-----------Backoffice END--------------#

@app.route('/single_mail' , methods = ["GET"])
def SingleEmail():
    i = 1
    email = request.args.get('email')
    user = BOModel().getUserdataToMail(email)
    if user :
        name     = user.full_name
        email    = user.email
        mobile   = user.mobile
        password = user.password
        user_id  = user.user_id
        if name :
            subject  = name + ", Your Login Credentials for TNOA 2021 Virtual"
        else:
            subject  = " Your Login Credentials for TNOA 2021 Virtual"
            
        html     = render_template('backoffice/email/tnoa_bulk_mail_1.html', name = name, email = email, mobile = mobile, password = password)    
        EMAIL.sendMail(subject,html,email)
        print(str(i) + ", " + user.full_name +  "," + user.email)
        return "Mail send Successfully"
    else :
        return "Email Not Registered ."  







