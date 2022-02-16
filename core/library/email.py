from flask import request, url_for,flash, render_template
from core import app
from flask import url_for
from datetime import datetime, date, time, timedelta
import requests,mandrill,json



class EMAIL:


# 	def sendMail(subject,html,to):
# 		MANDRILL_API_KEY='5MhjtQC-tCq5A9eYzuDpVg'
# 		mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
# 		# variable = render_template('users/email/registration_success_mail.html', name = user_name, email = email, password = password)

# 		message = { 'from_email': 'support@numerotec.com',
# 		'from_name': 'BOA MOS Summer Focus Virtual Symposium',
# 		'to': [{
# 				'email': to,
# 				'name': to,
# 				'type': 'to'
# 				},
# 				{
# 		         "email":"boamos2021backup@gmail.com",
# 		         "name":"BOA Backup",
# 		         "type":"bcc"
# 		      }],
# 		'subject': subject,
# 		'html': html
# 		}

# 		result = mandrill_client.messages.send(message = message)
# 		return ('success')

	def sendMail(subject,html,to):
		MANDRILL_API_KEY='MAoeFJshVAG4-xTyPpTgUg'
		mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
		message = {'subject' : subject, 'recipients':to,'from_name': 'MADRAS ICON 2021',
		'html': html, 'from_email' : 'support@numerotec.com', 
		'cc' : 'support@numerotec.com', 'Reply-To' : 'support@numerotec.com',
		"headers" :{"Reply-To": "support@numerotec.com"} ,'to' : [{'email':to,'name':to,'type':'to'},
		{'email':'tnoabackup@gmail.com','name':to,'type':'cc'}] }

		result = mandrill_client.messages.send(message = message,send_async=True)
		return ('success')


	def sendHelpDeskMail(subject,html,to):
		
		MANDRILL_API_KEY='5MhjtQC-tCq5A9eYzuDpVg'
		mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
		# variable = render_template('users/email/registration_success_mail.html', name = user_name, email = email, password = password)

		message = { 'from_email': 'support@numerotec.com',
		'from_name': 'BOA 2021, First Virtual Meet of BOA',

		'to': [{
				'email': 'support@numerotec.com',
				'name': to,
				'type': 'to'
				},
				],
		'subject': subject,
		'html': html,
		"headers": {
			"Reply-To": to
		},
		}

		result = mandrill_client.messages.send(message = message)
		# result is a dict with metadata about the sent message, including
		# if it was successfully sent
		
		return ('success')		

	# def sendMail(user_name,email,password):
	# support@numerotec.com
	# 	MANDRILL_API_KEY='7L0tswCIdGHr6oKi6IrW8A'
	# 	mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
	# 	variable = render_template('users/email/registration_success_mail.html', name = user_name, email = email, password = password)

	# 	message = { 'from_email': 'support@numerotec.com',
	# 	'from_name': 'STRAIGHT 2020, First Virtual Meet of SPOSI',
	# 	'to': [{
	# 			'email': email,
	# 			'name': user_name,
	# 			'type': 'to'
	# 			}],
	# 	'subject': "Dr."+user_name + " , Your registration is successful ",
	# 	'html': variable
	# 	}

	# 	result = mandrill_client.messages.send(message = message)
	# 	# result is a dict with metadata about the sent message, including
	# 	# if it was successfully sent
		
	# 	return ('success')

	# def sendMail(otp,otp_expiry_date,otp_expiry_time,am_or_pm,user_name,email):
	# 	MANDRILL_API_KEY='7L0tswCIdGHr6oKi6IrW8A'
	# 	mandrill_client=mandrill.Mandrill(MANDRILL_API_KEY)
	# 	variable = render_template('users/email/mail.html', otp = otp, otp_expiry_date = otp_expiry_date, otp_expiry_time = otp_expiry_time, am_or_pm = am_or_pm, name = user_name)
	# 	message = { 'from_email': 'support@numerotec.com',
	# 	'from_name': 'Straight 2020',
	# 	'to': [{
	# 	'email': email,
	# 	'name': user_name,
	# 	'type': 'to'
	# 	}],
	# 	'subject': "OTP for Straight 2020 - Virtual Conference of SPOSI",
	# 	'html': variable
	# 	}


	# 	result = mandrill_client.messages.send(message = message)
	# 	# result is a dict with metadata about the sent message, including
	# 	# if it was successfully sent
		
	# 	return ('success')
