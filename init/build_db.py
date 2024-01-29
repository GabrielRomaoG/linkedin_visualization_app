import sqlite3


def main():
    db_path = "src/data/processed/default_gabriel_data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open("init/schema.sql") as schema_file:
        schema_sql = schema_file.read()
        cursor.execute(schema_sql)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
