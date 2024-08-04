import sqlite3
from privacy import pathToWalletsDatabase


class WalletDatabase:
    def __init__ (self, chatID: int) -> None:
        self.__chatID: int = chatID;
        self.__connection = sqlite3.Connection(pathToWalletsDatabase);
        self.__cursor = self.__connection.cursor();

    def __del__ (self) -> None:
        self.__connection.close();
    
    def createWallet (self) -> None:
        self.__cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS '{self.__chatID}' 
            (channel_id INTEGER PRIMARY KEY, price REAL NOT NULL)
            """
        );
        self.__connection.commit();

    def insertChannel (self, channelID: int, price: float) -> None:
        self.__cursor.execute(
            f"""
            INSERT INTO {self.__chatID} (channel_id, price)
            VALUES (?, ?)
            """, (channelID, price)
        );
        self.__connection.commit();

    def deleteChannel (self, channelID: int) -> None:
        self.__cursor.execute(
            f"""
            DELETE FROM {self.__chatID}
            WHERE channel_id = ?
            """,
            (channelID,)
        );
        self.__connection.commit();

    def getAll (self) -> tuple[tuple[int, float]]:
        self.__cursor.execute(
            f"""
            SELECT *
            FROM {self.__chatID}
            """
        );
        return self.__cursor.fetchall();

    def isRegistered (self) -> bool:
        self.__cursor.execute(
            f"""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name='{self.__chatID}'              
            """);
        return (self.__cursor.fetchone() is not None);