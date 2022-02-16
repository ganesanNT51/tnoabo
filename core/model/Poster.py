from sqlalchemy import create_engine, MetaData, Table, insert, select,update,delete,text
from sqlalchemy.sql import and_, or_, distinct
from core import app
import datetime
from datetime  import datetime,date, timedelta,time
import json
import collections

engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)


# engine = create_engine('')
class Poster():	
	def __init__(self):
		try:
			self.meta = MetaData()
			self.poster = Table("poster", self.meta, autoload=True, autoload_with=engine)
		except Exception as e:
			print(e)

	def getposter(self):
		stmt = text('select distinct(date) from poster order by date')
		result = engine.execute(stmt)
		results = [dict(r) for r in result] if result else None
		# print(results)
		return results

	def posterarea(self,p_date):
		stmt = text('select * from poster where date = :p_date')
		result = engine.execute(stmt,p_date=p_date)
		results = [dict(r) for r in result] if result else None
		return results 

	def get_author_ppt(self,poster_id):
		stmt = select([self.poster])
		stmt = stmt.where(
			and_(
				self.poster.c.poster_id.in_([poster_id])
				)
			)
		results = engine.execute(stmt)
		result = results.fetchone()
		# print(result)
		return dict(result)