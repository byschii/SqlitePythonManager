import sqlite3
import subprocess 
import random

class SqliteMenager(object):
	def __init__(self, on_ram = False, db_file = None):
		assert (isinstance(on_ram,(bool))),"'on_ram' must be either True o False"
		if on_ram:
			self.db_name = None #does't have a name, its just in memory
			self.db = sqlite3.connect(':memory:')
			self.db_cur = self.db.cursor()
		else:

			assert (db_file and len(db_file)>4),"You must specify a correct name for the db file"

			if db_file[-3:] != '.db':
				db_file += '.db'

			self.db_name = db_file
			self.db = sqlite3.connect(db_file)
			self.db_cur = self.db.cursor()

	def is_legal_table(self,tbl):
		"""
		this method check is the TBL parameter represent or not actually a table  
		correct if = 
		list('name', list_columns( list_column('name','type','other') ))
		"""

		if not isinstance(tbl,(list)):
			return False
		else:
			if isinstance(tbl[0], (str)) and isinstance(tbl[1], (list)):
				for c in tbl[1]:
					if not isinstance(c,(list)):
						return False
					else:
						if not isinstance(c[0],(str)) or not isinstance(c[1],(str)) or not isinstance(c[2],(str)):
							return False
			else: 
				return False
	
		return True

	def db_full_schema(self):
		"""
		this function returns a main list that contains other lists
		each 'sub-list' represent a table -> each 'table' contains 3 elements
		the first is the table name, the secon is another list
		this last list contains a description of the columns
		each column is describes as a list with 3 elements
		the name, the type, and other details
		"""

		tables = subprocess.check_output('sqlite3 '+self.db+' .tables', shell=True)
		tables = tables.split()#nomi delle tabelle

		t = []

		for tbl in tables:
			s = (subprocess.check_output('sqlite3 '+self.db+' ".schema '+tbl+'"', shell=True)).split()[2:]
			s = ' '.join( s )
			s = s[:-1]
			t.append( s )

		tables = []

		for x in t:
			x = x[:-1]
			tb,dt = x.split('(')
			tb = tb.strip()
			dt = dt.split(',')
			f = []
			for g in dt:
				g = g.split()
				f.append([g[0], g[1], ' '.join(g[2:]) ])
			tables.append( [tb,f] )

		return tables

	def tbl_content(self, tbl_name = None, as_string = False):
		if not tbl_name:
			raise Exception("you must specify the name of the table")
		
		tbl = filter(lambda x: x[0] == tbl_name, self.db_full_schema())
		tbl = tbl[0][1]
		content = {}
		ris = self.cur.execute('select * from '+tbl_name).fetchall()

		stringa = ''
		for r in ris:
			stringa += 'insert into '+tbl_name+' values ('
			for v in r:
				stringa += 

		for t in zip(tbl,xrange(len(tbl))):
			content[t[0][0]] = [r[t[1]] for r in ris]
		
		if not as_string:
			return content
		else:
			return stringa







if __name__ == '__main__':
	man = SqliteMenager('test')


























