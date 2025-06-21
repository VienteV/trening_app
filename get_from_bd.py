import configparser
from calendar import month

import psycopg2
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Repetition:
    amount: int
    extra_weight: float
    repetition_id: int

@dataclass
class Exercese:
    exercese_id: int
    name: str
    description: str
    repetitions: list
    filepath: str

config = configparser.ConfigParser()
config.read('config')


class BD:
    conn = psycopg2.connect(dbname='trening_app', user='maksim',
                            password=config.get('data', 'dbpassword'), host='localhost')
    cur = conn.cursor()

    def get_exercese_for_trening(self, trening_id):
        self.cur.execute("""SELECT exercese_id FROM exercese 
        JOIN trening USING(trening_id)
        WHERE trening_id = %s """, (trening_id,))
        exercese = self.cur.fetchall()
        list_exercese = []
        for exercese_id in exercese:
            self.cur.execute("""SELECT  name, description, filename
            FROM exercese JOIN exercese_type USING(type_id)
            WHERE exercese_id = %s
            """, exercese_id)
            exer = self.cur.fetchone()

            self.cur.execute("""SELECT amount, extra_weight, repetition_id
            FROM repetition
            WHERE exercese_id = %s""", exercese_id)
            repetitions = self.cur.fetchall()
            repetition_list = []
            for repetition in repetitions :
                repetition_list.append(Repetition(*repetition))
            final_exercese = Exercese(exercese_id = exercese_id[0], name = exer[0], description=exer[1], repetitions= repetition_list, filepath=exer[-1])
            list_exercese.append(final_exercese)
        return list_exercese

    def get_typs(self, user = False, type_id = False):
        if type_id:
            self.cur.execute("""SELECT * FROM exercese_type WHERE type_id = %s""", (type_id,))
        elif not user:
            self.cur.execute("""SELECT * FROM exercese_type""")
        else:
            self.cur.execute("""SELECT exercese_type.type_id, exercese_type.name, exercese_type.description, filepath, filename FROM exercese_type 
            JOIN exercese USING(type_id)
            JOIN trening USING(trening_id)
            WHERE user_name = %s
            GROUP BY exercese_type.type_id
            ORDER BY exercese_type.name""", (user, ))
        types = self.cur.fetchall()
        return types

    def update_type(self, type_id ,name, description='', file_name = '', file_path = ''):
        try:
            self.cur.execute("""UPDATE exercese_type 
            SET name = %s,
             description = %s,
             filename = %s,
             filepath = %s
             WHERE type_id = %s""", (name, description, file_name , file_path, type_id))
            self.conn.commit()
        except Exception as e:
            return e

    def get_trening(self, user_name, date=False):
        if date is False:
            self.cur.execute("""SELECT * FROM trening WHERE user_name = %s""", (user_name, ))
        else:
            self.cur.execute("""SELECT * FROM trening WHERE update_time = %s AND user_name = %s""", (date, user_name))
        trenings = self.cur.fetchall()
        return trenings

    def get_all_repetitions_for_type(self, type_id, user_name):
        now = datetime.now()
        delta = timedelta(days=90)
        date = now - delta
        self.cur.execute("""SELECT update_time, SUM(amount), MAX(extra_weight)
        FROM exercese JOIN trening USING(trening_id)
        JOIN exercese_type USING(type_id)
        JOIN repetition USING(exercese_id)
        WHERE type_id = %s AND update_time > %s AND user_name = %s
        GROUP BY update_time
        ORDER BY update_time""", (type_id, date, user_name))
        repetitions = self.cur.fetchall()
        return repetitions

    def create_type(self, name, description='', file_name = '', file_path = ''):
        try:
            self.cur.execute("""INSERT INTO exercese_type(name, description, filename, filepath) 
            VALUES(%s, %s, %s, %s)""", (name, description, file_name, file_path))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return e

    def create_trening(self, update_time, user_name):
        try:
            self.cur.execute("""INSERT INTO trening(update_time, user_name) 
            VALUES(%s, %s) 
            RETURNING trening_id;""",(update_time, user_name))
            trening_id = self.cur.fetchone()[0]
            self.conn.commit()
            return trening_id
        except Exception as e:
            self.conn.rollback()
            return e

    def create_exercese(self, type_id, trening_id):
        try:
            self.cur.execute("""INSERT INTO exercese(type_id, trening_id)
            VALUES(%s, %s)
            RETURNING exercese_id""", (type_id, trening_id))
            exercese_id = self.cur.fetchone()[0]
            self.conn.commit()
            return exercese_id
        except Exception as e:
            self.conn.rollback()
            return e

    def create_repetition(self, exercese_id, amount, extra_weight):
        try:
            self.cur.execute("""INSERT INTO repetition(exercese_id, amount, extra_weight) 
            VALUES (%s,%s,%s)""", (exercese_id, amount, extra_weight))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return e

    def delete_exercese(self, exercese_id):
        try:
            self.cur.execute("""DELETE FROM repetition WHERE exercese_id = %s""", (exercese_id, ))
            self.cur.execute("""DELETE FROM exercese WHERE exercese_id = %s""", (exercese_id, ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
            return e

    def get_type_id(self, type_name):
        self.cur.execute("""SELECT type_id FROM exercese_type WHERE name = %s""", (type_name, ))
        type_id = self.cur.fetchone()
        return type_id

    def add_token(self, token):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS tokens (
        token text UNIQUE PRIMARY KEY,
        used BOOLEAN DEFAULT FALSE)""")
        self.conn.commit()
        try:
            self.cur.execute("""INSERT INTO tokens(token) VALUES (%s)""", (token, ))
            self.conn.commit()
            return True
        except:
            return False

    def give_tokens(self):
        try:
            self.cur.execute("""SELECT token FROM tokens WHERE used = FALSE""")
            tokens = self.cur.fetchall()
            tokens = [i[0] for i in tokens]
            return tokens
        except:
            return "empty"
    def use_token(self, token):
        self.cur.execute("""UPDATE tokens
        SET used = TRUE 
        WHERE token = %s""", (token,))
        self.conn.commit()

    def get_role(self, user_name):
        self.cur.execute("""SELECT role FROM users WHERE user_name = %s""", (user_name,))
        role = self.cur.fetchone()
        print(role)
        if role[0] == 'admin':
            return True
        else:
            return False

    def get_users(self):
        self.cur.execute("""SELECT user_name, role FROM users""")
        users = self.cur.fetchall()
        users = [{'name': i[0], 'role': i[1]} for i in users ]
        return users

    def set_role(self, user_name, role):
        self.cur.execute(("""UPDATE users SET role = %s 
        WHERE user_name = %s"""), (role, user_name))
        self.conn.commit()

    def delete_exercese_type(self, exercese_type_id):
        try:
            self.cur.execute("""DELETE FROM exercese_type WHERE type_id = %s""", (exercese_type_id, ))
        except:
            self.conn.rollback()
            try:
                self.cur.execute("""SELECT exercese_id FROM exercese WHERE type_id = %s""", (exercese_type_id,))
                exercese_ids = tuple(i[0] for i in self.cur.fetchall())
                self.cur.execute("""DELETE FROM repetition WHERE exercese_id IN %s""", (exercese_ids, ))
                self.cur.execute("""DELETE FROM exercese WHERE type_id = %s""", (exercese_type_id,))
                self.cur.execute("""DELETE FROM exercese_type WHERE type_id = %s""", (exercese_type_id,))
            except Exception as e:
                print(e)
                self.conn.rollback()
                return False
        self.conn.commit()
        return True