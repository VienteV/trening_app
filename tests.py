import unittest
import psycopg2
from datetime import datetime
from get_from_bd import BD
import configparser



config = configparser.ConfigParser()
config.read('config')

class TestForDBoperationd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bd = BD()

        cls.test_conn = psycopg2.connect(dbname='test_trening_app', user='maksim',
                            password=config.get('data', 'dbpassword'), host='localhost')
        cls.cur = cls.test_conn.cursor()
        cls.bd.conn = cls.test_conn
        cls.bd.cur = cls.cur
        cls.bd.cur.execute("""DROP TABLE repetition""")
        cls.bd.cur.execute("""DROP TABLE exercese""")
        cls.bd.cur.execute("""DROP TABLE trening""")
        cls.bd.cur.execute("""DROP TABLE exercese_type""")
        cls.bd.cur.execute("""DROP TABLE users""")
        cls.bd.conn.commit()

        cls.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                user_name VARCHAR(256) UNIQUE)""")

        cls.cur.execute("""CREATE TABLE IF NOT EXISTS exercese_type(
        	type_id int UNIQUE PRIMARY KEY 
        	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
        	name VARCHAR(256),
        	description TEXT)""")

        cls.cur.execute("""CREATE TABLE IF NOT EXISTS trening(
        	trening_id int UNIQUE PRIMARY KEY
        	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
        	update_time timestamp,
        	user_name VARCHAR(256),

        	FOREIGN KEY (user_name) REFERENCES users(user_name)
        ) """)

        cls.cur.execute("""CREATE TABLE IF NOT EXISTS exercese(
        	exercese_id int UNIQUE PRIMARY KEY
        	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
        	type_id INT,
        	trening_id INT,
        	FOREIGN KEY(type_id) REFERENCES exercese_type(type_id),
        	FOREIGN KEY(trening_id) REFERENCES trening(trening_id)
        ) """)

        cls.cur.execute("""CREATE TABLE IF NOT EXISTS repetition (
        	repetition_id int UNIQUE PRIMARY KEY 
        	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
        	exercese_id INT,
        	amount INT NOT NULL,
        	extra_weight FLOAT,
        	FOREIGN KEY(exercese_id) REFERENCES exercese(exercese_id)
        ) """)
        try:
            cls.cur.execute("""INSERT INTO users (user_name) VALUES
            ('user1'),
            ('user2');""")
        except:
            cls.bd.conn.commit()

        cls.cur.execute("""INSERT INTO exercese_type (name, description) VALUES
            ('Push-ups', 'Basic bodyweight exercise for upper body'),
            ('Squats', 'Basic lower body exercise'),
            ('Pull-ups', 'Upper body exercise using a bar');
            """)
        cls.cur.execute("""INSERT INTO trening (update_time, user_name) VALUES
            ('2023-10-01 10:00:00', 'user1'),
            ('2023-10-02 15:30:00', 'user2');""")
        cls.cur.execute("""INSERT INTO exercese (type_id, trening_id) VALUES
            (1, 1),  -- Push-ups для тренировки 1
            (2, 1),  -- Squats для тренировки 1
            (3, 2);  -- Pull-ups для тренировки 2""")
        cls.cur.execute("""INSERT INTO repetition (exercese_id, amount, extra_weight) VALUES
            (1, 10, 0.0),  -- 10 повторений для Push-ups
            (1, 15, 0.0),  -- 15 повторений для Push-ups
            (2, 20, 0.0),  -- 20 повторений для Squats
            (3, 8, 5.0);   -- 8 повторений для Pull-ups с дополнительным весом 5.0""")

    @classmethod
    def tearDownClass(cls):
        cls.bd.cur.execute("""DROP TABLE repetition""")
        cls.bd.cur.execute("""DROP TABLE exercese""")
        cls.bd.cur.execute("""DROP TABLE trening""")
        cls.bd.cur.execute("""DROP TABLE exercese_type""")
        cls.bd.cur.execute("""DROP TABLE users""")
        cls.bd.conn.close()


    def test_get_typs(self):
        print(self.bd.get_typs())
        self.assertEqual(type(self.bd.get_typs()), list)

    def test_get_exercese_for_trening(self):
        for i in range(1,5):
            print(self.bd.get_exercese_for_trening(i))
            self.assertEqual(type(self.bd.get_exercese_for_trening(i)), list)

    def test_get_trening(self):
        user_names = ['user1', 'user2', 'user3']
        for i in user_names:
            self.assertEqual(type(self.bd.get_trening(i)), list)

    def test_get_all_repetitions_for_type(self):
        user_names = ['user1', 'user2', 'user3']
        types =[1, 2, 4]
        for i in range(len(user_names)):
            self.assertEqual(type(self.bd.get_all_repetitions_for_type(types[i], user_names[i])), list)

    def test_create_type(self):
        len_types_before = len(self.bd.get_typs())
        self.bd.create_type(self, 'Name')
        len_types_after = len(self.bd.get_typs())
        self.assertEqual(len_types_after, len_types_before)

    def test_create_trening(self):
        update_time = datetime.now()
        for user_name in ['user1', 'user2']:
            self.assertEqual(type(self.bd.create_trening(update_time, user_name)), int)
        with self.assertRaises(Exception) as context:
            self.bd.create_trening(update_time, 'user3')

            self.assertIsInstance(context.exception, Exception)

    def test_create_exercese(self):
        for i in range(0):
            self.assertEqual(type(self.bd.create_exercese(i, i)), int)

    def test_create_repetition(self):
        self.bd.create_repetition(1, 1, 1)
        self.bd.create_repetition(7, 1, 1)

    def test_delete_exercese(self):
        self.bd.delete_exercese(1)




if __name__ == '__main__':
    unittest.main()