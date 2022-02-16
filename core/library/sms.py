from core import app
from flask import url_for
from datetime import datetime, date, time, timedelta
import requests,json
import urllib.parse


class SMS:
	# Usage : SMS().Send(['9952514049','8637643225'],'sms message')
	def Send(mobile, message):

	    url_sms = 'http://api.msg91.com/api/v2/sendsms'

	    data = {
	        "sender": "VRCOTP",
	        "route": "4",
	        "country": "91",
	        "sms": [
	            {
	                "message": urllib.parse.quote_plus(message),
	                "to": mobile
	            }
	        ]
	        
	    }

	    headers = { 

	        'authkey': "231926AE3o5GFOkdM5c110b52", #MSG91 Numerotec account API Key
	        'Content-Type': "application/json"
	    }
	    
	    response = requests.request("POST", url_sms, data=json.dumps(data),  headers=headers)
	    return('success')


# app.jinja_env.globals.update(SMS=SMS)