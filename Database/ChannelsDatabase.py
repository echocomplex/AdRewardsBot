import sqlite3
from privacy import pathToChannelsDatabase;


class ChannelsDatabase:
    def __init__ (self) -> None:
        self.__connection = sqlite3.Connection(pathToChannelsDatabase);
        self.__cursor = self.__connection.cursor();
    
    def __del__ (self) -> None:
        self.__connection.close();

    def add (self, channelID: int, channelName: str, price: float) -> None:
        self.__cursor.execute(
            """
            INSERT INTO channels (channel_id, channel_name, channel_link, price)
            VALUES (?, ?, ?)
            """, (channelID, channelName, price)
        );
        self.__connection.commit();

    def takeChannels (self) -> tuple[tuple[int, str, str, str]]:
        self.__cursor.execute(
            """
            SELECT *
            FROM users
            """
        );
        return self.__cursor.fetchall();

    def deleteChannel (self, channelLink: str) -> None:
        self.__cursor.execute(
            """
            DELETE FROM channels
            WHERE channel_link = ?
            """,
            (channelLink,)
        );
        self.__connection.commit();


if (__name__ == "__main__"):
    connection = sqlite3.Connection("Channels.db");
    cursor = connection.cursor();
    cursor.execute(
        """
        CREATE TABLE channels (INTEGER chat_id, TEXT language, REAL profit)
        """
    );
    connection.commit();
    connection.close();