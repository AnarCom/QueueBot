from peewee import *
from DbConnection import DbConn


class BaseModel(Model):
    class Meta:
        database = DbConn().connection


class Migration(BaseModel):
    id = AutoField(column_name='id')
    name = TextField(column_name='name', null=False)

    class Meta:
        table_name = 'migrations'


class User(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    name = TextField(column_name='name', null=True)

    class Meta:
        table_name = 'users'
