import string
from mig_list import migration_list as m_list
from entities import Migration


def prepare_env(cursor):
    print("Started migration: part [1] - migration tables")
    cursor.execute("""
    CREATE  TABLE IF NOT EXISTS migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name VARCHAR(20) NOT NULL 
    )
    """)


def execute_migration(cursor, name: string, sql: string) -> None:
    cursor.execute(f"""
    {sql}
    """)
    cursor.execute(f"""
    INSERT INTO migrations(name) VALUES (\'{name}\');
    """)


def execute_migrations(cursor):
    prepare_env(cursor=cursor)
    exec_all_migrations(cursor)


def exec_all_migrations(cursor):
    for i in m_list:
        print(f"executing transaction {i['name']}?")
        if not Migration.select().where(Migration.name == i['name']).exists():
            print('Y')
            execute_migration(cursor, i['name'], i['sql'])
        else:
            print('N')
