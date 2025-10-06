import configparser

import psycopg2


config = configparser.ConfigParser()
config.read('config')

conn = psycopg2.connect(dbname='trening_app', user='maksim',
                        password=config.get('data', 'dbpassword'), host='localhost')
cur = conn.cursor()
cur.execute("""DROP TABLE CARDS""")

conn.commit()