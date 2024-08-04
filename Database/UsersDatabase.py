import sqlite3
from privacy import pathToUsersDatabase


class UsersDatabase:
    def __init__ (self, chatID: int) -> None:
        self.__chatID: int = chatID;
        self.__connection = sqlite3.Connection(pathToUsersDatabase);
        self.__cursor = self.__connection.cursor();

    def __del__ (self) -> None:
        self.__connection.close();

    def addUser (self) -> None:
        self.__cursor.execute(
            """
            INSERT OR IGNORE INTO users (chat_id, language) 
            VALUES (?, ?)
            """,
            (self.__chatID, "RU"));
        self.__connection.commit();

    def takeUsers (self) -> tuple:
        self.__cursor.execute(
            """
            SELECT chat_id
            FROM users
            """);
        users: list = [];
        data: list = self.__cursor.fetchall();
        for row in data:
            users.append(row[0]);
        return tuple(users);

    def takeLanguage (self) -> str:
        self.__cursor.execute(
            """
            SELECT language 
            FROM users 
            WHERE chat_id = ?
            """,
            (self.__chatID,));
        language: str = self.__cursor.fetchone()[0];
        return language;

    def updateLanguage (self, language: str) -> None:
        self.__cursor.execute(
            """
            UPDATE users 
            SET language = ?
            WHERE chat_id = ?
            """,
            (language, self.__chatID));
        self.__connection.commit();


if (__name__ == "__main__"):
    connection = sqlite3.Connection("Users.db");
    cursor = connection.cursor();
    cursor.execute(
        """
        CREATE TABLE users (chat_id INTEGER PRIMARY KEY, language TEXT NOT NULL)
        """
    );
    connection.commit();
    connection.close();
