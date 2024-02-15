from src.infra.db.test_resources.build_test_db.build_test_db import (
    build as build_test_db,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path


class DBConnectionHandler:
    current_directory = Path(__file__).resolve().parent
    test_db_path = current_directory / "test.db"

    def __init__(self) -> None:
        self.__connection_string = "{}:///{}".format(
            "sqlite",
            self.test_db_path,
        )
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @classmethod
    def delete_db(cls):
        os.remove(cls.test_db_path)

    @classmethod
    def build_db(cls):
        build_test_db(cls.test_db_path)
