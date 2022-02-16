from sqlalchemy import create_engine, select, MetaData, Table
from sqlalchemy.sql import and_, or_
from core import app
from datetime import datetime

engine = create_engine(app.config['DATABASE_URI'],pool_size=5000,max_overflow=100,pool_pre_ping=True,pool_recycle=3600)

# engine = create_engine('')
class Log():	
	def __init__(self):
		try:
			self.meta = MetaData()
			self.logs = Table("logs", self.meta, autoload=True, autoload_with=engine)
		except Exception as e:
			print(e)
	
	def insert(self,data):
		conn = engine.connect()
		print('inside model insert log')
		result = conn.execute(self.logs.insert(), data)
		conn.close()
		return result
