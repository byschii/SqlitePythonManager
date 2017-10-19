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
		if self.in_ram or self.db_name == 'cat_s_secrets.db':
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

	def db_full_schema(self, as_string= False):
		"""
		this function returns a main list that contains other lists
		each 'sub-list' represent a table -> each 'table' contains 3 elements
		the first is the table name, the secon is another list
		this last list contains a description of the columns
		each column is describes as a list with 3 elements
		the name, the type, and other details
		"""

		tables = subprocess.check_output('sqlite3 '+self.db_name+' .schema', shell=True)
		if as_string:
			return tables

		tables = tables.split('\n')[:-1]#nomi delle tabelle


		t = []

		for x in tables:
			x = x[:-1]
			split_index = x.find('(')
			x = [ x[:split_index].split()[2] , x[split_index+1:][:-1].split(',') ]

			t.append(x)

		tables = t
		t = []

		for name,rows in tables:
			name = name.strip()

			rows = map(lambda x: x[1:] if x[0] == ' ' else x,rows)
			rows = map(lambda x: x[:-1] if x[-1] == ' ' else x,rows)

			rows = map(lambda x: [x.split()[0] , x.split()[1] , x.split(x.split()[1])[1][1:]] , rows)

			t.append([name,rows])

		tables = t
		
		return tables



	
	def test_tbl_content(self, name = None, as_ = None):
		raise Exception("NOT TO USE!!")
		if not name:
			raise Exception("you must specify the name of the table")
		
		tbl = filter(lambda x: x[0] == name, self.db_full_schema())
		tbl = tbl[0][1] # lista delle colonne della tablella
		content = {}
		ris = self.db_cur.execute('select * from '+name).fetchall()



			
		if isinstance(as_,(dict)):
			for col,indx in zip(tbl,xrange(len(tbl))):
				content[col[0]] = [r[indx] for r in ris]

			return content


		if isinstance(as_,(str)):
			stringa = ''
			for r in ris:
				stringa += 'insert into '+name+' values ('
				for v in r:
					if isinstance(v,(unicode)):
						v = "\'"+v.encode("utf-8")+"\'"
					stringa += (str(v)+',')
				stringa = stringa[:-1] + ');'
			return stringa
	






if __name__ == '__main__':
	from placeholder import build

	build()
	db_menager = SqliteMenager('cat_s_secrets')

	print '--E--N--D--'
	for t in db_menager.db_full_schema():
		print t
	del db_menager


	







