from flask import request, Blueprint, jsonify, redirect, url_for,flash, render_template
from core.model.CertModel import CertModel
from core.model.Sessions import Sessions
from random import randint
import datetime
from datetime import timedelta,date,datetime
import requests, mandrill, json
from .. import Helper,Cryptography,current_app
from datetime import timedelta
from flask import session, app
import ast

import os
from os.path import join, dirname, realpath
from flask import send_file,send_from_directory,safe_join
import base64

app = Blueprint('certify', __name__)

@app.route('/certificate', methods = ["GET", "POST"])
def Certificate():
	c = CertModel()
	if session.get('user'):
		user = session.get('user')
		user_id = user['user_id']
		print(str(user_id))
		res   =   c.get_certificate_count(user_id)
		cert_count = res[0]
		#encrypted_user_id= Cryptography.encrypt(user_id)
		data = c.get_certificate_data(user_id)

	#return render_template('certificate/certificate.html' ,data = data,user_id =encrypted_user_id)
	return render_template('certificate/certificate.html' , cert_count=cert_count, data = data,user_id =user_id,Cryptography=Cryptography)


@app.route('/cert_download/<certificate_id>', methods = ["GET", "POST"])
def Cert_Download(certificate_id):
	c = CertModel()
	#certificate_id= Cryptography.decrypt(certificate_id)
	cert = c.get_cert_data(certificate_id)
	print(cert)
	cert_type = cert['cert_type']
	filename = cert['cert_name']
	user_id = cert['user_id']
	uploads = os.path.join(current_app.root_path, "static/pdf/",cert_type)
	print(uploads)
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
	cert = CertModel()
	update_time = cert.update_download_time(user_id,filename,dt_string)
	# return "test"
	return send_from_directory(directory=uploads, filename=filename,as_attachment=True)
	# return send_from_directory(directory="D:\GIT\sposi\core/static/pdf", filename="Judge50.pdf",as_attachment=True)
	
	


