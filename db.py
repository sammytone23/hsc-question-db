# db funcs

import sqlite3

class SQL():
	def __init__(self,db):
		self.path=db

	def execute(command):
		firstword=command.split()[0]
		if firstword in ['SELECT', 'INSERT']:
			con=sqlite3.connect(self.path)
			cur=con.cursor()
			result=cur.execute(command)
			con.commit()
			con.close()
			return result
		else:
			con=sqlite3.connect(self.path)
			con.execute(command)
			con.commit()
			con.close()
			return False