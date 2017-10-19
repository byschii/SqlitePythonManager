import sqlite3

def build():
	print "+-------------------------------------------------------"
	print "| creating a db with some cats and their plans for taking over the world"
	print "| database name : 'cat_s_secrets' "
	print "| "
	print "| we are assuming there is no other 'cat_s_secrets' "
	print "+-------------------------------------------------------"

	conn = sqlite3.connect('cat_s_secrets.db')
	cur = conn.cursor()
	cur.execute(" create table cat (serial integer primay key, name text, plan_id integer references plan ( id ), hair_color text, birdth date);")
	conn.commit()
	cur.execute(" create table plan ( id integer primay key, day_by date, accomplices integer, description text);")
	conn.commit()
	ins_cat = 'insert into cat values ( ? , ? , ? , ? , ? )'
	ins_plan = 'insert into plan values ( ? , ? , ? , ? )'

	data_cat = [
			(11,'ugo',5,'blue','1988-06-11'),
			(74,'jerry',22,'black','1999-01-30'),
			(7,'carl',None,'black','2000-05-17'),
			(63,'nemo',15,'red','2001-09-11'),
			(45,'floyd',None,'pink','1970-12-24')
			]

	data_plan = [
			(5,'2007-10-10',13,'wants to ally with a pirate crew'),
			(22,'1991-08-6',0,'wants to create the internet'),
			(15,'2025-01-01',0,'just use a simple big bomb')
			]

	cur.executemany(ins_cat,data_cat)
	conn.commit()

	cur.executemany(ins_plan,data_plan)
	conn.commit()