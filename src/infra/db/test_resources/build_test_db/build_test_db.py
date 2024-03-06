import sqlite3
import os


def build(db_path: str):
    try:
        os.remove(db_path)
    except OSError:
        pass
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(
        "src/infra/db/test_resources/build_test_db/init_db/init.sql"
    ) as schema_file:
        schema_sql = schema_file.read()
        sql_statements = schema_sql.split(";")
        for statement in sql_statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

    conn.commit()
    conn.close()
