from flask import request, Blueprint, jsonify,session,url_for,redirect,render_template
from core.model.Sessions import Sessions
from random import randint
# import datetime
from datetime import timedelta,date,datetime,time

# import datetime
app = Blueprint('s_chart', __name__)

@app.route('send_sess_chat', methods=['GET','POST'])
def send_sess_chat():
   user = session["user"]
   room = request.form['session_id']
   incom_user_id = request.form['user_id']
   msg = request.form['msg']
   my_user_id = user.get('user_id')
   comment_data = {
            'user_id' : incom_user_id,
            'session_id' :room ,
            'comment' :msg,
            'created_at': datetime.now(),
        }
   # print(data)
   s = Sessions()
   save_comment = s.save_comment(comment_data)
   print(save_comment)
   return jsonify({'status':1})
   # emit('receved_message', {'msg' : msg,'incom_user_id':incom_user_id},room=room) 

@app.route('receved_message', methods=['GET','POST'])
def receved_message():
   session_id = request.form['session_id']
   my_user_id = request.form['my_user_id']
   msg_last_dt = request.form['msg_last_dt']
   # print("msg_last_dt")
   # print(msg_last_dt)
   # user_id = user.get('user_id')
   html = ""
   s = Sessions()
   comments = s.get_last_comments(msg_last_dt,session_id)
   msg_last_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
   msg_last_dt_disc = s.get_last_comment_dt(session_id)
   if msg_last_dt_disc:
      msg_last_dt = msg_last_dt_disc['created_at'].strftime("%Y-%m-%d %H:%M:%S")
   # print("comments")
   # print(comments)
   # print(my_user_id)
   for comment in comments:
      # print(comment.get('user_id'))
      if comment.get('user_id') == int(my_user_id):
         msg_type="outgoing"
           #    outgoint msg
         html += render_template("hall_screen/sess_chat/outgoing_msg.html",comment=comment)
      else:
         msg_type="incoming"
           # incomping msg   
         html += render_template("hall_screen/sess_chat/incoming_msg.html",comment=comment)
   return jsonify({'status':1,'html':html,'msg_last_dt':msg_last_dt})   


@app.route('receved_message_by_date_hall', methods=['GET','POST'])
def receved_message_by_date_hall():
   s_date = request.form['s_date']
   s_hall = request.form['s_hall']
   my_user_id = request.form['my_user_id']
   msg_last_dt = request.form['msg_last_dt']
   
   html = ""
   s = Sessions()
   comments = s.get_last_comments_by_date_hall(msg_last_dt,s_date,s_hall)
   msg_last_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
   msg_last_dt_disc = s.get_last_comment_dt_by_date_hall(s_date,s_hall)
   if msg_last_dt_disc:
      msg_last_dt = msg_last_dt_disc['created_at'].strftime("%Y-%m-%d %H:%M:%S")
   # print("comments")
   # print(comments)
   # print(my_user_id)
   for comment in comments:
      # print(comment.get('user_id'))
      if comment.get('user_id') == int(my_user_id):
         msg_type="outgoing"
           #    outgoint msg
         html += render_template("hall_screen/sess_chat/outgoing_msg.html",comment=comment)
      else:
         msg_type="incoming"
           # incomping msg   
         html += render_template("hall_screen/sess_chat/incoming_msg.html",comment=comment)
   return jsonify({'status':1,'html':html,'msg_last_dt':msg_last_dt})      


@app.route('getcomments/<int:session_id>/<int:user_id>', methods=['GET','POST'])
def getcomment(session_id,user_id):
   user = session.get("user")
   # user_id = 0;
   html = ""
   msg = ""
   status = 0
   if user:
      # user_id = user.get('user_id')
      s = Sessions()
      valid = True
      results = s.getcomment(session_id)
      msg_last_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
      msg_last_dt_disc = s.get_last_comment_dt(session_id)
      if msg_last_dt_disc:
         msg_last_dt = msg_last_dt_disc['created_at'].strftime("%Y-%m-%d %H:%M:%S")

      for r in results:
         # print(user_id)
         # print("r user_iddddd")
         # print(r['user_id'])
         if r.get('user_id') == user_id:
            html = html + render_template('hall_screen/sess_chat/outgoing_msg.html',comment=r)
            # print('Outgoing html')
            # print(html)
            status = 1
         else:
            html = html + render_template('hall_screen/sess_chat/incoming_msg.html',comment=r)
            # print('incoming html')
            # print(html)
            status = 1
   return {'status':status,'html':html,'user_id':user_id,'msg_last_dt':msg_last_dt}   


@app.route('getcomment_by_date_hall/<s_date>/<s_hall>/<int:user_id>', methods=['GET','POST'])
def getcomment_by_date_hall(s_date,s_hall,user_id):
   user = session.get("user")
   # user_id = 0;
   html = ""
   msg = ""
   status = 0
   if user:
      # user_id = user.get('user_id')
      s = Sessions()
      valid = True
      results = s.getcomment_by_date_hall(s_date,s_hall)
      msg_last_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
      msg_last_dt_disc = s.get_last_comment_dt_by_date_hall(s_date,s_hall)
      if msg_last_dt_disc:
         msg_last_dt = msg_last_dt_disc['created_at'].strftime("%Y-%m-%d %H:%M:%S")

      for r in results:
         # print(user_id)
         # print("r user_iddddd")
         # print(r['user_id'])
         if r.get('user_id') == user_id:
            html = html + render_template('hall_screen/sess_chat/outgoing_msg.html',comment=r)
            # print('Outgoing html')
            # print(html)
            status = 1
         else:
            html = html + render_template('hall_screen/sess_chat/incoming_msg.html',comment=r)
            # print('incoming html')
            # print(html)
            status = 1
   return {'status':status,'html':html,'user_id':user_id,'msg_last_dt':msg_last_dt}      
   
      
	