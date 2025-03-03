import psycopg2

import psycopg2
conn = psycopg2.connect(dbname='trening_app', user='maksim',
                        password='4132', host='localhost')
cur = conn.cursor()

cur.execute("""CREATE TABLE exercese_type(
	type_id int UNIQUE PRIMARY KEY 
	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
	name VARCHAR(256),
	description TEXT)""")

cur.execute("""CREATE TABLE trening(
	trening_id int UNIQUE PRIMARY KEY
	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
	update_time timestamp
) """)

cur.execute("""CREATE TABLE exercese(
	exercese_id int UNIQUE PRIMARY KEY
	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
	type_id INT,
	trening_id INT,
	
	FOREIGN KEY(type_id) REFERENCES exercese_type(type_id),
	FOREIGN KEY(trening_id) REFERENCES trening(trening_id)
) """)

cur.execute("""CREATE TABLE repetition (
	repetition_id int UNIQUE PRIMARY KEY 
	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
	exercese_id INT,
	amount INT NOT NULL,
	extra_weight FLOAT,
	
	FOREIGN KEY(exercese_id) REFERENCES exercese(exercese_id)
) """)

conn.commit()