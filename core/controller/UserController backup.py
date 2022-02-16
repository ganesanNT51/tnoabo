from flask import request, Blueprint, jsonify, redirect, url_for,flash, render_template
from core.model.User_details import User_details
from core.model.CertModel import CertModel
from core.model.Sessions import Sessions
from random import randint
import datetime
from datetime import timedelta,date,datetime
import requests, mandrill, json
from .. import Helper,Cryptography
from datetime import timedelta
from flask import session, app

from core.library.sms import SMS
from core.library.email import EMAIL


app = Blueprint('user', __name__)

@app.route('/testcrypt', methods = ["GET", "POST"])
def encryptdecrypt():
    encrypted = Cryptography.encrypt(1)
    decrypted = Cryptography.decrypt(encrypted)
    return encrypted + "<br />" +decrypted
    
    


@app.route('/test', methods = ["GET", "POST"])
def Test():
    return render_template('users/email/mail.html', name = 'Ganesan' ,otp='123456' ,otp_expiry_date= '2020-12-18',otp_expiry_time='18:00:00',am_or_pm ='PM')

@app.route('/success', methods = ["GET", "POST"])
def Success():
    return render_template('users/email/registration_success_mail.html', name = 'Ganesan' ,email='ganesan@numerotec.com',password='12587')

@app.route('/sposi', methods = ["GET", "POST"])
def Landing():
    return render_template('landing.html')
    

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True

    # return redirect(url_for('user.Login'))
#home page or main page based on session..
@app.route('/', methods = ["GET", "POST"])
def Home():
    # s = Sessions()
    if request.method == "GET":
      
        status = 1
        if session.get('user'):
            try:
                user = session.get('user')
                print('in session')
                user_id = user['user_id']
                # the below line comment by ganesan
                # user_id = request.args.get('user_id')
                encrypted_user_id= Cryptography.encrypt(user_id)
                # current_session = s.getCurrentSession()
                # session_id =  current_session['session_id']
                return redirect (url_for('user.Lobby',user_id= encrypted_user_id))   
                # return render_template('users/home.html', user = user ,user_id=encrypted_user_id)
            except:
                return render_template('users/login_screen.html')
        else:
            print('in main page')
            return render_template('users/login_screen.html')
        

@app.route('/register')
def Register():
    print('ín form')
    us = User_details()
    # countries = us.get_countries()
    # states = us.get_states()
    # print('states')
    # print(states)
    data=None
    return render_template('users/registration.html',data=data)

@app.route('/login')
def Login():
    print('ín form')
    return render_template('users/login_screen.html')  


# Forgot password..
@app.route('forgot_password')
def Forgot_password():
    return render_template('users/forgot_password_screen.html') 

@app.route('verify_otp/<user_id>')
def Verify_otp(user_id):
    return render_template('users/otp_screen.html',user_id = user_id)

#Reset_password
@app.route('reset_password/<int:user_id>')
def Reset_password(user_id):
    print('In reset password function')
    return render_template('users/reset_password_screen.html' ,user_id =user_id)  

@app.route('post_reset_password'  , methods = ["GET","POST"])
def Post_reset_password():
    if request.method == "POST":
        print('In post reset password')
        new_password = request.form['new_password']
        print( "new Password is = "   + new_password)
        confirm_new_password = request.form['confirm_new_password']
        id = request.form['user_id']
        if ( not new_password or not confirm_new_password ):
            flash('Please enter password / confirm password')            
            return redirect (url_for('user.Reset_password',user_id= id))
        if  (new_password  == confirm_new_password):
            flash('Your password reset successful.')
            us = User_details()
            reset_pass = us.update_password(id,new_password,confirm_new_password)
            return redirect (url_for('user.Login',user_id= id))   
        else:
            flash('Passwords do not match') 
            return redirect (url_for('user.Reset_password',user_id= id))      
            # return render_template('users/reset_password_screen.html',user_id = user_id)         

@app.route('postverify_otp' , methods = ["GET","POST"])
def PostVerify_otp():
    # otp_number
    print('In post verify function')
    if request.method == "POST":
        
        form_otp = request.form['otp_number']
        id = request.form['user_id']
        print(id)
        print(form_otp )
        if ( not form_otp ) :
            msg = "Please enter the OTP sent to you"
            flash("Please enter the OTP sent to you")
            return redirect (url_for('user.Verify_otp' ,user_id = id))
        else:
            us = User_details()
            #get user details from DB..
            
            print(id)
            user_output = us.get_users_id(id)
            #fetching datas for validation..
            db_otp = user_output['otp']
            db_otp_expiry_at = user_output['otp_expiry_at']
            print(db_otp)
            print(db_otp_expiry_at)

            if (int(form_otp) == int(db_otp)   and datetime.now() < db_otp_expiry_at):
                status = 1
                # user_state_country = us.get_state_and_country_names(id)
                #adding state and country name to user dict..
                # user_output['state_name'] = user_state_country['state_name']
                # user_output['country_name'] = user_state_country['name']
                # print(user_output['country_name'])
                
                # session['user'] =  user_output
                # return to reset password
                # return redirect (url_for('user.Home',user_id= id))  
                return redirect (url_for('user.Reset_password',user_id= id))

            if (int(form_otp) == int(db_otp)   and datetime.now() > db_otp_expiry_at):
                status = 0
                flash('OTP Expried !')
                return redirect (url_for('user.Forgot_password'))
            else:
                print('Invalid OTP')
                flash('Invalid OTP')
                return redirect (url_for('user.Verify_otp' ,user_id = id))

# function to validate otp entered by user 

def otp_validation(id,form_otp):

    us = User_details()
    #get user details from DB..
    user_output = us.get_users_id(id)
    #fetching datas for validation..
    db_otp = user_output['otp']
    db_otp_expiry_at = user_output['otp_expiry_at']

    if (int(form_otp) == int(db_otp)   and datetime.now() < db_otp_expiry_at):
        status = 1
        user_state_country = us.get_state_and_country_names(id)
        #adding state and country name to user dict..
        user_output['state_name'] = user_state_country['state_name']
        user_output['country_name'] = user_state_country['name']
        
        session['user'] =  user_output
        # return to reset password
        return redirect (url_for('user.Home',user_id= id))  

    if (int(form_otp) == int(db_otp)   and datetime.now() > db_otp_expiry_at):
        status = 0
        flash('OTP Expried !')
        return redirect (url_for('user.Forgot_password'))
    else:
        return redirect (url_for('user.Forgot_password'))


        

# PostForgot_password
@app.route('postForgot_password' , methods = ["GET","POST"])
def PostForgot_password():
     if request.method == "POST":
        form_email = request.form['email']
        form_mobile = request.form['mobile']
        print("Given Email  : " +  form_email)
        print("Given Mobile  : " +  form_mobile)
        us = User_details()
        if(not form_email and not form_mobile):
            flash("Please enter email or mobile")
            print("Please enter email or mobile")
            return redirect (url_for('user.Forgot_password'))
        if (not form_email):
            print('Mobile exist')
            user_output = us.get_users_mobile_data(form_mobile)
        if(not form_mobile):
            user_output = us.get_users_email_data(form_email)
    
        emptyArray = []
        print(user_output)
        if (user_output == emptyArray or user_output is None):
            flash("The given Email or Mobile doesn't exist")
            return redirect (url_for('user.Forgot_password')) 
        else :
            user_id  = user_output['user_id']
            email  = user_output['email']     # added on Dec 3 2020
            otp_number = generate_otp(user_id)
            if otp_number != 'failed':
                #calling function to send the generated otp to users mail and mobile number..
                #fetch otp fields from return value..
                otp = otp_number['otp']
                otp_created_at = otp_number['otp_created_at']
                otp_expiry_at = otp_number['otp_expiry_at']
                user_name = otp_number['full_name']
                mobile = otp_number['mobile']
                email = otp_number['email']

                #separating otp expiry date and time..
                otp_expiry_date = otp_expiry_at.strftime("%d/%m/%y")
                otp_expiry_time = otp_expiry_at.strftime("%H:%M:%S")

                #mention AM or PM..
                am_or_pm = otp_expiry_time[:2]
                
                if int((am_or_pm)) >= 12:
                    am_or_pm = 'PM'
                else:
                    am_or_pm = 'AM'

                subject= "OTP for BOA 2021 - Virtual Conference of BOA"
                html = render_template('users/email/mail.html', otp = otp, otp_expiry_date = otp_expiry_date, otp_expiry_time = otp_expiry_time, am_or_pm = am_or_pm, name = user_name)    
                # mail_otp = Send_mail(otp,otp_expiry_date,otp_expiry_time,am_or_pm,user_name,email)
                # mail_otp = EMAIL.sendMail(otp,otp_expiry_date,otp_expiry_time,am_or_pm,user_name,email)
                EMAIL.sendMail(subject,html,email)
            
                #calling function to send the generated otp to users mail and mobile number..
                #preparing text message before sending otp message to users mobile..
                if user_name:
                    msg = "Dear Dr. "+user_name+","+"\n"+"One Time Password (OTP) for BOA 2021 login is "+str(otp)+"."+"\n"+"Your OTP is valid untill "+str(otp_expiry_date)+" "+str(otp_expiry_time)+" "+am_or_pm+"."
                else:
                    msg = "Hi,"+"\n"+" Your One Time Password (OTP) for BOA 2021 login is "+str(otp)+"."+"\n"+"Your OTP is valid untill "+str(otp_expiry_date)+" "+str(otp_expiry_time)+" "+am_or_pm+"."
                # sms_otp = send_sms(form_mobile, msg)
                print(msg)
                sms_otp    = SMS.Send([mobile],msg)

                # if mail_otp and sms_otp == 'success':
                if  sms_otp == 'success':
                    msg = "Please enter the 4 digit OTP sent to your email id : "+email[:3]+"xxx@xxx.xx and mobile : "+mobile[:3]+"xxxxx"+mobile[-3:]
                    # html = render_template('users/otp_page.html', id = id, message = msg)
                    return redirect (url_for('user.Verify_otp',mobile = form_mobile, user_id = user_id,email = form_email)) 
                else:
                    status = 0
                    msg = "Issue in sending OTP . Please click resend OTP or try after sometime."    
                
                print("mobile number exitst ")
                flash("mobile number exitst")


                # return redirect (url_for('user.Verify_otp',mobile = form_mobile, user_id = user_id)) 
                return redirect (url_for('user.Forgot_password'))
                
        return redirect (url_for('user.Forgot_password'))

    

  




    

            

# Post_login1 
@app.route('/post_login', methods = ["GET","POST"])
def Post_login():
    print('ín form')
    if request.method == "POST":
        form_email = request.form['email']
        form_password = request.form['password']
        if  not form_email  or not form_password:
            flash('Please enter email and password')
            return redirect (url_for('user.Login'))
        else :
            us = User_details()
            user_output = us.get_users_email_data(form_email)
            if user_output : 
                print("form input password " + form_password)
                db_pass =  user_output['password']
                print(" db password " + db_pass )
                if form_password == db_pass:
                    print(user_output['password'] + "and given password is " + form_password )
                    user_id = user_output['user_id']
                    print(  user_id )

                    us.update_last_login(user_id,datetime.now());
                    
                    session['user'] =  user_output
                    encrypted_user_id= Cryptography.encrypt(user_id)
                    print(encrypted_user_id)
                    # flash('Regsitration Successfully Saved ! ' )
                    return redirect (url_for('user.Home',user_id= encrypted_user_id)) 

                    # return jsonify({'status':status, 'user_id':user_id})
                else : 
                    status = 0
                    # msg = "Passsword invalid. Please check the password."
                    flash('Passsword invalid. Please check the password.  ' )
                    return redirect (url_for('user.Login'))

            else:
                status = 0
                msg = "Email id is not registered."

            flash("Email id is not registered." )
            return redirect (url_for('user.Login'))   
            # return jsonify({'status':status, 'message':msg})


    return render_template('users/login_screen.html') 

def generate_otp(id):

    msg = ""
    us = User_details()
    
    #generating 4 digit otp number..
    otp = randint(1000,9999)

    #fetching current date and time for otp and setting 10 minutes for otp expiry before inserting into db..
    otp_created_at = datetime.now()
    otp_expiry_at = otp_created_at + timedelta(minutes = 10)

    data = {
        'otp':otp,
        'otp_created_at':otp_created_at,
        'otp_expiry_at':otp_expiry_at
    }

    #updating the new otp for existing user in db..
    user_output = us.update_user_otp(id,otp,otp_created_at,otp_expiry_at)

    #once updated fetching the user record..  only for checking
    user_output = us.get_users_id(id)

    if user_output:
        return (user_output)
    else:
        return('failed')


@app.route('/post_register', methods = ["GET","POST"])
def Post_register():
    if request.method == "POST":
        # print('in post')
        now = datetime.now()
        # print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        password  = request.form['password']
        confirm_password = request.form['confirm_password']
        form_email = request.form['email_id']
        form_mobile = request.form['mobile']
        prefix = request.form['prefix']
        full_name = request.form['name']

        # fetching data from form..
        data = {
            'prefix'     : request.form['prefix'],
            'full_name' : request.form['name'],
            'city' : request.form['city'],
            'state' :request.form ['state'],
            'email' : request.form['email_id'],
            'mobile' : request.form['mobile'],
            'password' : request.form['password'],
            'confirm_password' : request.form['confirm_password'],
            # 'country' :request.form ['country'],
            # 'affiliation'  : request.form['affiliation'],
            'mcn_number'  : request.form['mcn_number'],
            'mc_state'  : request.form['mc_state'],
            'created_at' :[dt_string]
        }

        #ceating object for model class..
        us = User_details()
        # print('data')
        # print(data)
        #calling insert method using that object..
        if(password  == confirm_password):
            check_email = us.get_users_email(form_email)
            check_mobile = us.get_users_mobile(form_mobile)
            if (check_email == "success"):
                flash('Email Already Exists.')
                return render_template('users/registration.html',data=data)
                # return redirect (url_for ('user.Register'))
            if (check_mobile == "success"):
                flash('Mobile Number Already Exists.')
                return render_template('users/registration.html',data=data)
                # return redirect (url_for ('user.Register'))
            else:
                insert_users = us.insert_users(data)
                if insert_users:
                    success_msg = "Dear " + prefix +full_name  + '\n\n' + "Thank you for registering for BOA 2021, the annual meet of BOA. For your records, your user name is " + form_email + " and password is " + password + " . "+'\n\n' + "The above information has also been sent to your email id. Please check your spam / promotions folder if you don't see it the main in your inbox."+ '\n\n'+ "For assistance, please write to support@numerotec.com."
                    SMS.Send([form_mobile],success_msg)
                    
                    subject = "Welcome to BOA 2021. First Annual Virtual Conference of BOA"
                    html = render_template('users/email/registration_success_mail_2.html', name = full_name, email = form_email, password = password)
                    # subject = "Dr."+full_name + " , Your registration is successful"
                    # html = render_template('users/email/registration_success_mail.html', name = full_name, email = form_email, password = password) 
                    EMAIL.sendMail(subject,html,form_email)
                    flash('Registration Successfully . An email and SMS has been sent to you.')
                    return redirect (url_for('user.Register'))
        else:
            flash('Password and confirm password mismatch ')
            # return redirect (url_for('user.Register'))  
            return render_template('users/registration.html')          

#states dropdown option based on cuntry selected..
@app.route('/states_dropdown_1/<int:country_id>')
def States_dropdown(country_id):
    us = User_details()
    status = 0
    msg = "" 
    html = '<option value = "" id = "select"> --Select-- </option>'
   
    states = us.get_states(country_id)
    if states:
        status = 1
        for state in states:
            html += "<option value = "+  str(state.get("state_id"))+">"+ str(state.get("state_name")) +"</option>"
   
    return jsonify({'status':status, 'html':html})


# logout 
@app.route('logout', methods = ["GET", "POST"])
def Logout():
    session.pop('user')
    session.pop('_flashes', None)
    return redirect(url_for('user.Login'))

@app.route('/profile/<user_id>' , methods = ["GET"])
def Profile(user_id):
    print('ín form')
    us = User_details()
    countries = us.get_countries()
    user_data = us.edit_profile(user_id)
    return render_template('users/profile.html',countries = countries, user_data=user_data)

@app.route('/profile' , methods = ["POST"])
def ProfilePost():
    print('ín POST Profile function ')
    us = User_details()
    countries = us.get_countries()
    return render_template('users/profile.html',countries = countries)

@app.route('/faculty' , methods = ["GET"])
def Faculty():
    print('In facult get function')
    status = 1
    if session.get('user'):
        user = session.get('user')
        print("in session logged in")
        user_id = request.args.get('user_id')
        encrypted_user_id= Cryptography.encrypt(user_id)
        us = User_details()
        faculties = us.get_faculty()
        return render_template('faculty/faculty_index.html',faculties = faculties)
    else :


        print('No session login')
        return redirect (url_for('user.Login'))

# @app.route('/lobby/<string:user_id>' , methods = ["GET"])
@app.route('/lobby' , methods = ["GET"])
def Lobby():
    #  s = Sessions()
    c = CertModel()
    status = 1
    if session.get('user'):    
        user = session.get('user')
        print("in session logged in")
        user_id = request.args.get('user_id')
        res   =   c.get_certificate_count(user.get('user_id'))
        cert_count = res[0]
        encrypted_user_id= Cryptography.encrypt(user_id)        
        # print("count")
        # print(count)
        
        # c_session = s.getCurrentSession()
        # print('current session')
        # print(c_session)
        # session_id =  c_session['session_id']
        return render_template('users/lobby_links.html', cert_count = cert_count,user_id = encrypted_user_id)
    else :
        
        return redirect (url_for('user.Login'))

@app.route('/helpdesk' , methods = ["GET"])
def HelpDesk():
     status = 1
     if session.get('user'):
        
        user = session.get('user')
        print("in session logged in")
        user_id = user['user_id']
        encrypted_user_id= Cryptography.encrypt(user_id)
        print(user_id)
        print(encrypted_user_id)
        # session.pop('_flashes', None)
        us = User_details()
        userdata = us.get_userdata(user_id)
        return render_template('users/help_desk.html',user_id = user_id,userdata =userdata)
     else :
        
        return redirect (url_for('user.Login'))

@app.route('/helpdesk' , methods = ["POST"])
def PostHelpDesk():
    now = datetime.now()
    full_name  = request.form['full_name']
    email      = request.form['email']
    mobile     = request.form['mobile']
    feedback   = request.form['feedback']
    user_id    = request.form['user_id']
    dt_string  = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {
            'full_name' : full_name,
            'email' : email,
            'mobile' : mobile,
            'feedback' :feedback,
            'user_id'  : user_id,
            'created_at' :[dt_string]
        }
    us = User_details()
    save_feedback = us.insert_feedback(data)
    subject = "SPOSI STRAIGHT 2020  - Help Desk feedback from  " "Dr."+full_name 
    html = render_template('users/email/help_desk_mail.html', name = full_name, email = email, mobile=mobile, feedback = feedback)    

    EMAIL.sendHelpDeskMail(subject,html,email )
    flash('Thank you for submitting your query / feedback here.If it’s a query you have raised here , please be assured that we’ll revert in a couple of hours')
    return redirect (url_for('user.HelpDesk'))

    # return redirect (url_for('user.Home'))

@app.route('/bulkemail' , methods = ["GET"])
def BulkEmail():
    us = User_details()
    users = us.get_users()
    for user in users:
        name=user.full_name
        email =user.email
        mobile=user.mobile
        password=user.password
        user_id = user.user_id
        subject = "Welcome to STRAIGHT 2020. First Annual Virtual Conference of SPOSI"
        html = render_template('users/email/bulkmail_2.html', name = name, email = email, mobile = mobile, password = password)    
        EMAIL.sendMail(subject,html,email)
        print(user.full_name)

        # now = datetime.now()
        # dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        # update_send_mail_time = us.update_mailsend_time(user_id,dt_string)

    return "success"

    




    
                              
