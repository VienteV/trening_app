import configparser

import psycopg2


config = configparser.ConfigParser()
config.read('config')

conn = psycopg2.connect(dbname='trening_app', user='maksim',
                        password=config.get('data', 'dbpassword'), host='localhost')
cur = conn.cursor()
cur.execute("""DROP TABLE CARDS""")
cur.execute("""CREATE TABLE IF NOT EXISTS cards(
	card_id int UNIQUE PRIMARY KEY 
	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
	category VARCHAR(20) CHECK (category IN ('python', 'sql', 'git', 'networking', 'other')),
	main_side VARCHAR(256),
	other_side TEXT,
	points INT DEFAULT(0)""")
cur.execute("""INSERT INTO cards (category, main_side, other_side, points) VALUES
('python', 'Что такое GIL?', 'Global Interpreter Lock - механизм, который позволяет выполнять только один поток Python за раз в процессе CPython.', 0),
('sql', 'В чем разница BETWEEN и IN?', 'BETWEEN для диапазона значений, IN для списка конкретных значений.', 0);""")
conn.commit()