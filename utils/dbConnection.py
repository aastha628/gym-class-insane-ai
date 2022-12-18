import psycopg2
import json


class Database:

    conn = None

    @staticmethod
    def getInstance():
        if Database.conn == None:
            try:
                Database.conn = psycopg2.connect(
                    database="gym_app", user='gym_user', password='some_secure_key', host='localhost')
            except Exception as e:
                print(e)
        return Database.conn
