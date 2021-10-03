migration_list = [
    {
        "name": "create-person-tables",
        "sql": """
        CREATE TABLE IF NOT EXISTS users (
        id UNSIGNED BIG INT PRIMARY KEY ,
        name VARCHAR(255)
        );
        """
    },
    {
        "name": "create-queue-table",
        "sql": """
        CREATE TABLE IF NOT EXISTS queue(
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            user_id UNSIGNED BIG INT ,
            foreign key (user_id) REFERENCES users(id)
        );
        """
    }
]
