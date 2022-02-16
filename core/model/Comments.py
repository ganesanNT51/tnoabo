from sqlalchemy import create_engine, MetaData, Table, insert, select,update,delete,text
from sqlalchemy.sql import and_, or_, distinct
from core import app
import datetime
from datetime  import datetime,date, timedelta,time
import json
import collections

engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)


# engine = create_engine('')
class Comments():	
	def __init__(self):
		try:
			self.meta = MetaData()
			self.comments = Table("comments", self.meta, autoload=True, autoload_with=engine)
		except Exception as e:
			print(e)

	def get_comments(self):
		conn = engine.connect()
		stmt = text('select c.*,u.*,s.*,c.created_at from comments c inner join users u on u.user_id=c.user_id inner join sessions s on s.session_id = c.session_id order by c.created_at desc')
		result = conn.execute(stmt)
		conn.close()
		results = [dict(r) for r in result] if result else None
		return results 


	def rejectcomment(self, comment_id):
		conn = engine.connect()
		stmt = select([self.comments])
		stmt = stmt.where(
			and_(
				self.comments.c.comment_id.in_([comment_id]),
			)
		)
		result = conn.execute(stmt)
		conn.close()
		return result.rowcount

	def saveisreject(self, comment_id, data):
		conn = engine.connect()
		stmt = self.comments.update()
		stmt = stmt.where(
			and_(
				self.comments.c.comment_id.in_([comment_id]),
			)
		)
		result = conn.execute(stmt,data)
		conn.close()
		return result.rowcount