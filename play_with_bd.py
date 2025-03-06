
import psycopg2
conn = psycopg2.connect(dbname='trening_app', user='maksim',
                        password='4132', host='localhost')
cur = conn.cursor()

from bcrypt import hashpw, gensalt, checkpw
cur.execute("""INSERT INTO trening(update_time) VALUES('2024-12-16')""")
conn.commit()
'''
password = 'Mn3598sd'
salt = gensalt(rounds=12)  # Фактор стоимости = 12
hashed = hashpw(password.encode(), salt)
print(hashed)
cur.execute("""INSERT INTO users(user_name, password) VALUES(%s, %s)""", ('Viente', hashed))
conn.commit()
print("Данные успешно добавлены в таблицы!")'''