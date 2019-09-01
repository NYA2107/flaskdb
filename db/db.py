import pymysql

class Connection:
	def __init__(self):
		self.db = pymysql.connect("localhost","root","","flaskdb" )

	def change(self, sql):
		cursor = self.db.cursor()
		try:
			cursor.execute(sql)
			self.db.commit()
			msg = 'success'
		except:
			self.db.rollback()
			msg = 'error'
		return msg

	def read(self, sql):
		cursor = self.db.cursor()
		try:
			cursor.execute(sql)
			self.db.commit()
			results = cursor.fetchall()
		except:
			results = ('error')
		return results

	def close(self):
		self.db.close()

