import sqlite3


def main():
    db_path = "src/data/processed/linkedin_data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open("init/schema.sql") as schema_file:
        schema_sql = schema_file.read()
        sql_statements = schema_sql.split(";")
        for statement in sql_statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
