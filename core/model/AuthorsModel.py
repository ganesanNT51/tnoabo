from sqlalchemy import create_engine, MetaData, Table, insert, select,update,delete,text
from sqlalchemy.sql import and_, or_, distinct
from core import app
import datetime
from datetime  import datetime,date, timedelta,time
import json
import collections


engine = create_engine(app.config['DATABASE_URI'],pool_pre_ping=True, pool_size=32, max_overflow=64)


class AuthorsModel():
	def __init__(self):
		try:
			self.meta = MetaData()
			self.sessions = Table("sessions", self.meta, autoload=True, autoload_with=engine)
			self.comments = Table("comments", self.meta, autoload=True, autoload_with=engine)
			self.users = Table("users", self.meta, autoload=True, autoload_with=engine)
			self.s_attendance = Table("s_attendance", self.meta, autoload=True, autoload_with=engine)
			self.users_answer = Table("users_answer", self.meta, autoload=True, autoload_with=engine)
			
			self.authors = Table("authors", self.meta, autoload=True, autoload_with=engine)
			# self.categories = Table("categories", self.meta, autoload=True, autoload_with=engine)
			self.roles = Table("roles", self.meta, autoload=True, autoload_with=engine)
		except Exception as e:
			print(e)

	def getRoles(self):
		conn = engine.connect()
		stmt = select([self.roles])
		result = conn.execute(stmt)
		conn.close()
		results = [dict(r) for r in result] if result else None
		return results  

	# getAuthorsData  
	def getAuthorsData(self,search_input):
		conn = engine.connect()
		if search_input:
			stmt = text("select * from users where email  like" +"'%"+search_input+"%'" + " or  mobile like " +"'%"+search_input+"%'" + " or full_name like " +"'%"+search_input+"%'" +";" )
			result = conn.execute(stmt)
			conn.close()
			results = [dict(r) for r in result] if result else None
			return results
		else:
			return None    

	def getAuthor(self,author_id):
		conn = engine.connect()
		stmt = text("select * from authors where author_id= :author_id;" )
		result = conn.execute(stmt,author_id=author_id)
		conn.close()
		results = [dict(r) for r in result] if result else None
		if results:
			return results

		else :
			return None    		


	def getSeletedAuthors(self,user_id):
		conn = engine.connect()
		stmt = self.users.select().where(self.users.c.user_id.in_([user_id]))
		result = conn.execute(stmt)
		conn.close()
		return result  


	def insert_authors(self,data):
		conn = engine.connect()
		result = conn.execute(self.authors.insert(), data)
		conn.close()
		return result 

	def getSeletedAuthorsForSession(self,session_id):
		conn = engine.connect()
		print("Inside model get selected autors for session")
		print(session_id)
		stmt = text("select a.* ,s.session_title  ,r.role from authors a inner join  roles r on r.role_id = a.role_id inner join sessions s on s.session_id = a.session_id where a.session_id = " + str(session_id) + " ;")
		print(stmt)
		result = conn.execute(stmt)
		conn.close()
		return result

	def delete_authors(self,author_id):
		conn = engine.connect()
		safe_delete_stmt = text("SET SQL_SAFE_UPDATES = 0;")
		result_1 = conn.execute(safe_delete_stmt)
		
		stmt = text("delete from  authors  where author_id = :author_id;")
		# stmt = self.authors.delete().where(self.authors.c.user_id.in_([user_id]))
		result = conn.execute(stmt,author_id=author_id)
		conn.close()
		return result  

	def EditAuthorsForSession(self,user_id,session_id):
		conn = engine.connect()
		stmt = text("select a.* ,s.session_title  ,r.role from authors a inner join  roles r on r.role_id = a.role_id inner join sessions s on s.session_id = a.session_id where a.session_id = " + str(session_id) + " and a.user_id = "+ str(user_id) + " ;")
		result = conn.execute(stmt)
		conn.close()
		return result 

	def UpdateSelectedAuthors(self,author_id,data):
		conn = engine.connect()
		# self.contact_table.update().where(self.contact_table.c.contact_id.in_([id])).values(data)
		stmt =  self.authors.update()
		stmt = stmt.where(
			and_(
					self.authors.c.author_id.in_([author_id])
			)
		).values(data)
		result = conn.execute(stmt) 
		conn.close()
		# print(results)
		return result	                       
	