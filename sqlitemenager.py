import sqlite3
import subprocess 

class SqliteMenager(object):
	def __init__(self, db_location = None):
		assert (db_location and len(db_location)>4),"You must specify a correct name for the db file"

		if db_location == ':memory:':
			self.in_ram = True
			self.db_name = 'tmp_memory_db.db'
			
		else:
			if db_location[-3:] != '.db':
				db_location += '.db'

			self.db_name = db_location
			self.in_ram = False

		self.db = sqlite3.connect(self.db_name)
		self.db_cur = self.db.cursor()

	def __del__(self):
		"""
		this methos is called when you DEL the object and AT EXIT
		it only delete the file that stores temporanelay the db on memory 
		"""
		if self.in_ram:
			subprocess.call('rm '+self.db_name, shell = True)


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

		tables = subprocess.check_output('sqlite3 '+self.db_name+' .tables', shell=True)
		tables = tables.split()#nomi delle tabelle

		t = []

		for tbl in tables:
			s = (subprocess.check_output('sqlite3 '+self.db_name+' ".schema '+tbl+'"', shell=True)).split()[2:]
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
				if isinstance(v,(unicode)):
					v = v.encode("utf-8")

				stringa += (str(v)+',')

			stringa = stringa[:-1] + ')'


		for t in zip(tbl,xrange(len(tbl))):
			content[t[0][0]] = [r[t[1]] for r in ris]
		
		if not as_string:
			return content
		else:
			return stringa







if __name__ == '__main__':
	db_menager = SqliteMenager(':memory:')
	import time
	time.sleep(4)
	del db_menager


	


	'''
	per fate tutte le op sulla memory
	basta che lo apro cmq su file
	e che mi salvo il fatto che dovrebbe essere su memoria
	e quindi alla chiusuta cancello il file
	'''











