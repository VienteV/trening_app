import pytest
from datetime import datetime
from get_from_bd import *

@pytest.fixture(scope="session")
def bd():
    bd = BD()

    test_conn = psycopg2.connect(dbname='test_trening_app', user='maksim',
                                     password=config.get('data', 'dbpassword'), host='localhost')
    cur = test_conn.cursor()
    bd.conn = test_conn
    bd.cur = cur
    try:
        bd.cur.execute("""DROP TABLE repetition""")
        bd.cur.execute("""DROP TABLE exercese""")
        bd.cur.execute("""DROP TABLE trening""")
        bd.cur.execute("""DROP TABLE exercese_type""")
        bd.cur.execute("""DROP TABLE users""")
        bd.conn.commit()
    except:
        bd.conn.rollback()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_name VARCHAR(256) UNIQUE)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS exercese_type(
            	type_id int UNIQUE PRIMARY KEY 
            	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
            	name VARCHAR(256),
            	description TEXT,
            	filename TEXT,
            	filepath TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS trening(
            	trening_id int UNIQUE PRIMARY KEY
            	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
            	update_time timestamp,
            	user_name VARCHAR(256),

            	FOREIGN KEY (user_name) REFERENCES users(user_name)
            ) """)

    cur.execute("""CREATE TABLE IF NOT EXISTS exercese(
            	exercese_id int UNIQUE PRIMARY KEY
            	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
            	type_id INT,
            	trening_id INT,
            	FOREIGN KEY(type_id) REFERENCES exercese_type(type_id),
            	FOREIGN KEY(trening_id) REFERENCES trening(trening_id)
            ) """)

    cur.execute("""CREATE TABLE IF NOT EXISTS repetition (
            	repetition_id int UNIQUE PRIMARY KEY 
            	GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
            	exercese_id INT,
            	amount INT NOT NULL,
            	extra_weight FLOAT,
            	FOREIGN KEY(exercese_id) REFERENCES exercese(exercese_id)
            ) """)
    try:
        cur.execute("""INSERT INTO users (user_name) VALUES
                ('user1'),
                ('user2');""")
    except:
        bd.conn.commit()

    cur.execute("""INSERT INTO exercese_type (name, description) VALUES
                ('Push-ups', 'Basic bodyweight exercise for upper body'),
                ('Squats', 'Basic lower body exercise'),
                ('Pull-ups', 'Upper body exercise using a bar');
                """)
    cur.execute("""INSERT INTO trening (update_time, user_name) VALUES
                ('2023-10-01 10:00:00', 'user1'),
                ('2023-10-02 15:30:00', 'user2');""")
    cur.execute("""INSERT INTO exercese (type_id, trening_id) VALUES
                (1, 1),  -- Push-ups для тренировки 1
                (2, 1),  -- Squats для тренировки 1
                (3, 2);  -- Pull-ups для тренировки 2""")
    cur.execute("""INSERT INTO repetition (exercese_id, amount, extra_weight) VALUES
                (1, 10, 0.0),  -- 10 повторений для Push-ups
                (1, 15, 0.0),  -- 15 повторений для Push-ups
                (2, 20, 0.0),  -- 20 повторений для Squats
                (3, 8, 5.0);   -- 8 повторений для Pull-ups с дополнительным весом 5.0""")

    yield bd

    bd.cur.execute("""DROP TABLE repetition""")
    bd.cur.execute("""DROP TABLE exercese""")
    bd.cur.execute("""DROP TABLE trening""")
    bd.cur.execute("""DROP TABLE exercese_type""")
    bd.cur.execute("""DROP TABLE users""")
    bd.conn.close()


def test_get_typs(bd):
    a = bd.get_typs()
    print(bd.get_typs)
    assert a == [(1, 'Push-ups', 'Basic bodyweight exercise for upper body', None, None), (2, 'Squats', 'Basic lower body exercise', None, None), (3, 'Pull-ups', 'Upper body exercise using a bar', None, None)]

def test_get_exercese_for_trening(bd):
    trening_id = bd.get_trening('user1')

    a  = bd.get_exercese_for_trening(trening_id[0][0])
    assert a == [Exercese(exercese_id=1, name='Push-ups', description='Basic bodyweight exercise for upper body',
                          repetitions=[Repetition(amount=10, extra_weight=0.0, repetition_id=1),
                                       Repetition(amount=15, extra_weight=0.0, repetition_id=2)], filepath=None),
                 Exercese(exercese_id=2, name='Squats', description='Basic lower body exercise',
                          repetitions=[Repetition(amount=20, extra_weight=0.0, repetition_id=3)], filepath=None)]

def test_update_type(bd):
    bd.update_type(1, 'balagamba', 'very effective movement', '1', '1')
    bd.cur.execute("""SELECT * FROM exercese_type WHERE type_id = 1""")
    check = bd.cur.fetchall()[0]
    assert check == (1, 'balagamba', 'very effective movement', '1', '1')

def test_get_trening(bd):
    check = bd.get_trening('user1')
    assert check == [(1, datetime(2023, 10, 1, 10, 0), 'user1')]

def test_get_all_repetitions_for_type(bd):
    bd.create_trening(datetime.now(), 'user1')
    bd.cur.execute(f'''SELECT trening_id FROM trening WHERE update_time = (SELECT MAX(update_time) FROM trening)''')
    test_data = bd.cur.fetchone()
    bd.create_exercese('1', test_data[0])
    bd.create_repetition('4', '1', '1')
    check = bd.get_all_repetitions_for_type(1, 'user1')
    assert check[0][1:] == (1, 1.0, 'balagamba')