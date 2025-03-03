import psycopg2


class BD:
    conn = psycopg2.connect(dbname='trening_app', user='maksim',
                                password='4132', host='localhost')
    cur = conn.cursor()

    def get_exercese_for_trening(self, trening_id):
        self.cur.execute("""SELECT * FROM exercese 
        JOIN trening USING(trening_id)
        WHERE trening_id = %s """, (trening_id,))

        exercese = self.cur.fetchall()
        return exercese

    def get_typs(self):
        self.cur.execute("""SELECT * FROM exercese_type""")
        types = self.cur.fetchall()
        return types

    def get_trening(self):
        self.cur.execute("""SELECT * FROM trening""")
        trenings = self.cur.fetchall()
        return trenings

    def create_type(self, name, description=''):
        try:
            self.cur.execute("""INSERT INTO exercese_type(name, description) 
            VALUES(%s, %s)""", (name, description))
        except Exception as e:
            return e

    def create_trening(self, update_time):
        self.cur.execute("""INSERT INTO trening(update_time) VALUES(%s)""", (update_time))

    def create_exercese(self, type_id, trening_id):
        try:
            self.cur.execute("""INSERT INTO exercese(type_id, trening_id)
            VALUES(%s, %s)""", (type_id, trening_id))
            return True
        except Exception as e:
            return e

    def create_repetition(self, exercese_id, amount, extra_weight):
        try:
            self.cur.execute("""INSERT INTO repetition(exercese_id, amount, extra_weight) 
            VALUES (%s,%s,%s)""", (exercese_id, amount, extra_weight))
        except Exception as e:
            return e

a = BD()
print(a.get_exercese_for_trening(2))