import configparser
from calendar import month

import psycopg2
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Repetition:
    amount: int
    extra_weight: float

@dataclass
class Exercese:
    name: str
    description: str
    repetitions: list


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
            self.cur.execute("""SELECT  name, description
            FROM exercese JOIN exercese_type USING(type_id)
            WHERE exercese_id = %s
            """, exercese_id)
            exer = self.cur.fetchone()

            self.cur.execute("""SELECT amount, extra_weight 
            FROM repetition
            WHERE exercese_id = %s""", exercese_id)
            repetitions = self.cur.fetchall()
            repetition_list = []
            for repetition in repetitions :
                repetition_list.append(Repetition(*repetition))
            final_exercese = Exercese(name = exer[0], description=exer[1], repetitions= repetition_list)
            list_exercese.append(final_exercese)
            column_names = [desc[0] for desc in self.cur.description]
        return list_exercese

    def get_typs(self):
        self.cur.execute("""SELECT * FROM exercese_type""")
        types = self.cur.fetchall()
        return types

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

    def create_type(self, name, description=''):
        try:
            self.cur.execute("""INSERT INTO exercese_type(name, description) 
            VALUES(%s, %s)""", (name, description))
            self.conn.commit()
        except Exception as e:
            return e

    def create_trening(self, update_time, user_name):
        self.cur.execute("""INSERT INTO trening(update_time, user_name) 
        VALUES(%s, %s) 
        RETURNING trening_id;""",(update_time, user_name))
        trening_id = self.cur.fetchone()[0]
        self.conn.commit()
        return trening_id

    def create_exercese(self, type_id, trening_id):
        try:
            self.cur.execute("""INSERT INTO exercese(type_id, trening_id)
            VALUES(%s, %s)
            RETURNING exercese_id""", (type_id, trening_id))
            exercese_id = self.cur.fetchone()[0]
            self.conn.commit()
            return exercese_id
        except Exception as e:
            return e

    def create_repetition(self, exercese_id, amount, extra_weight):
        try:
            self.cur.execute("""INSERT INTO repetition(exercese_id, amount, extra_weight) 
            VALUES (%s,%s,%s)""", (exercese_id, amount, extra_weight))
            self.conn.commit()
        except Exception as e:
            return e
