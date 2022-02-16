from flask import session
from sqlalchemy import create_engine, select, MetaData, Table,text
from sqlalchemy.sql import and_, or_
from core import app
import boto3
from botocore.exceptions import ClientError

engine = create_engine(app.config['DATABASE_URI'],pool_recycle=3600)


class CertModel():	
	def __init__(self):
		try:
			self.meta = MetaData()
			self.users = Table("users", self.meta, autoload=True, autoload_with=engine)
			self.certificate = Table("certificate_2020", self.meta, autoload=True, autoload_with=engine)
		except Exception as e:
			print(e)

	def get_certificate_data(self, user_id):
		print('in Get Function')
		stmt = text("select u.user_id,u.full_name,c.id,c.cert_type, c.cert_name,c.title from users u left join  certificate_2020 c on c.user_id = u.user_id where is_present = 1 and u.user_id = "+ str(user_id) +";")
		result = engine.execute(stmt)
		return result	

	def update_download_time(self,user_id,filename,dt_string):
		stmt = text("update certificate_2020 set download_on = "+"'"+dt_string+"'"+ " where user_id = " +"'" +user_id+ "'"+" and cert_name= " +"'" +filename +"'"+";")
		print(stmt)
		result = engine.execute(stmt)
		return result
	
	def get_certificate_count(self, user_id):
		print('in count Function')
		stmt = text("select count(c.cert_name) as cert_count from certificate_2020 c where is_present = 1 and user_id = "+ str(user_id) +";")
		#print(stmt)
		result = engine.execute(stmt)
		res    =   [dict(r) for r in result] if result else None
		# print ("res")
		# print (res)
		return res
	
	def get_cert_data(self, certificate_id):
		print('cert_id')
		stmt = text("select * from certificate_2020 c where is_present = 1 and c.id = "+ str(certificate_id) +";")
		result = engine.execute(stmt)
		res    =   [dict(r) for r in result] if result else None
		print(res)
		return res[0]