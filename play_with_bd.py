from psycopg2 import sql
from datetime import datetime, timedelta
import random
import psycopg2

cur = conn.cursor()

cur.execute("""ALTER TABLE trening
ADD COLUMN user_name VARCHAR(256),
ADD CONSTRAINT fk_user_name
FOREIGN KEY (user_name) REFERENCES users(user_name);""")
conn.commit()


['exercese_id', 'type_id', 'trening_id', 'name', 'description', 'repetition_id', 'amount', 'extra_weight']
print("Данные успешно добавлены!")
'''
password = 'Mn3598sd'
salt = gensalt(rounds=12)  # Фактор стоимости = 12
hashed = hashpw(password.encode(), salt)
print(hashed)
cur.execute("""INSERT INTO users(user_name, password) VALUES(%s, %s)""", ('Viente', hashed))
conn.commit()
print("Данные успешно добавлены в таблицы!")'''