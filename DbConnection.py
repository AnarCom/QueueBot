from peewee import *


class DbConn:
    __instance = None
    connection = None
    cursor = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.connection = SqliteDatabase('queue_bot.sqlite')
            cls.cursor = cls.connection.cursor()
        return cls.__instance

    # closes connection to db at deleting object
    def __del__(self):
        self.connection.close()



