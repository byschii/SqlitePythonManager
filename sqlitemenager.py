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
			subprocess.check_call('rm '+self.db_name, shell = True)


	def is_legal_table(self,tbl):
		"""
		this method check is the TBL parameter represent or not actually a table  
		correct if = 
		list('name', list_columns( list_column('name','type','other') ))
		"""

		if not isinstance(tbl,(list)):#each table is a list
			return False
		else:
			if isinstance(tbl[0], (str)) and isinstance(tbl[1], (list)): # with a name(str), and some columns(list)
				for c in tbl[1]:#each column
					if not isinstance(c,(list)): # has to be a list
						return False
					else:
						if not isinstance(c[0],(str)) or not isinstance(c[1],(str)) or not isinstance(c[2],(str)): # containing exactly 3 strings
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
			t.append( s ) # riempio t con tutti i dati delle tabelle nel db

		tables = []

		for x in t:
			x = x[:-1]
			brach_index = x.find('(')
			dt , tb = x[brach_index:][:-1] , x[:brach_index][:-1] #nel primo metto nome tbl nel secondo i dati

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
		ris = self.db_cur.execute('select * from '+tbl_name).fetchall()

		stringa = ''
		for r in ris:
			stringa += 'insert into '+tbl_name+' values ('
			for v in r:
				if isinstance(v,(unicode)):
					v = "\'"+v.encode("utf-8")+"\'"

				stringa += (str(v)+',')

			stringa = stringa[:-1] + ');'


		for t in zip(tbl,xrange(len(tbl))):
			content[t[0][0]] = [r[t[1]] for r in ris]
		
		if not as_string:
			return content
		else:
			return stringa







if __name__ == '__main__':
	from placeholder import build

	build()
	db_menager = SqliteMenager('cat_s_secrets')

	print db_menager.tbl_content('cat',True)
	del db_menager


	







