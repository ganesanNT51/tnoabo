from core import app
from flask import url_for, session, redirect
from datetime import datetime, date, time, timedelta
from functools import wraps

# Flask View decorators
class RouteGroup:
	def bo_login_required(f):
		@wraps(f)
		def wrap(*args, **kwargs):
			# if user is not logged in, redirect to login page      
			if session.get('backoffice'):
				return f(*args, **kwargs)
			else:
				return redirect(url_for('backoffice.BOLogin'))
		return wrap

	# def profile_required(f):
	# 	@wraps(f)
	# 	def wrap(*args, **kwargs):
	# 		u=User()
	# 		user = session.get('user')
	# 		user_id = user.get('user_id')
	# 		user = User().get_user(user_id)
	# 		is_profile_update = user.get('is_profile_update')
	# 		print(str(is_profile_update))
	# 		# return str(is_profile_update)
	# 		if is_profile_update != 1 :
	# 			return redirect(url_for('user.UserProfile',user_id= user_id))
	# 		else :
	# 			return f(*args, **kwargs)

	# 	return wrap    

	# def payment_required(f):
	# 	@wraps(f)
	# 	def wrap(*args, **kwargs):
	# 		p = Payment()
	# 		user = session.get('user')
	# 		user_id = user.get('user_id')
	# 		checkpayment = p.checkuserinpayment(user_id)
	# 		# return len(checkpayment)
	# 		if (len(checkpayment)) == 1 :
	# 			return f(*args, **kwargs)
	# 		else:
	# 			return redirect(url_for('payupayment.payment'))
	# 	return wrap

	

# Controller Sample :
# from flask import request, Blueprint, jsonify, redirect, url_for,flash, render_template
# from core.library.route_group import RouteGroup


# @app.route('/home' , methods = ["GET"])
# @RouteGroup.login_required #check if login else automatically redirect to login page
# def home():
#       return "welcome home"

# @app.route('/payment' , methods = ["GET"])
# @RouteGroup.login_required #check if login else automatically redirect to login page
# @RouteGroup.payment_required #check if payment done else  automatically redirect to payment page
# def payment():
#       return "payment page here"