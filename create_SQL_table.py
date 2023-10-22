import pandas as pd
import mysql.connector
from mysql.connector import Error
from parsed_data_from_log import Graph


class MSQFileParsed(Graph):
    """Class for processing and importing data from a log file into a MySQL database."""

    def __init__(self) -> None:
        """Initialize the MSQFileParsed object with default values."""
        super().__init()
        self._counter: int = 0
        self.host: str = "localhost"
        self.user: str = "user"
        self.password: str = "Qwer@123456789"
        self.database: str = "client_log"
        self.table_name: str = "log3"
        self.columns: list = ['decodedFrames', 'lossFrame', 'lossPacket', 'realFrames', 'receivedFrames', 'time']
        self.log_file_path = 'bstr_client.log'
        self.csv_file: str = None

    def create_connection(self) -> None:
        """Create a connection to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
            return connection  # Return True if the connection is successful
        except Error as e:
            print(f"Error: {e}")

    def create_table(self, connection):
        """Create a table in the database to store the log data."""
        try:
            cursor = connection.cursor()
            formatted_columns = [col.lower().replace(' ', '_') for col in self.columns]
            columns_with_types = [f"{col} VARCHAR(255)" for col in formatted_columns]
            columns_str = ', '.join(columns_with_types)

            create_table_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_str}"

            cursor.execute(create_table_query)
            connection.commit()
            print(f"Table {self.table_name} created successfully")
        except Error as e:
            print(f"Error: {e}")

    def table_filling(self, connection, tables_data: dict):
        """Fill the database table with data from the log file."""
        cursor = connection.cursor()
        _counter: int = 0
        while any(tables_data.values()):
            try:
                message_keys = list(tables_data.keys())
                poped_value = []
                for key, values_list in tables_data.items():
                    if values_list:
                        removed_value = values_list.pop()
                        poped_value.append(removed_value)
                        # print(f"Removed value {removed_value} from key '{key}'")

                # Construct the SQL query with actual values
                columns = ', '.join(message_keys)
                values = ', '.join(map(str, poped_value))
                sql_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
                print(f"SQL command is -{sql_query}")

                # Execute the SQL query
                cursor.execute(sql_query)

                connection.commit()
            except KeyError as e:
                print(f"KeyError: {e}")
            except mysql.connector.Error as err:
                print(f"MySQL Connector Error: {err}")
                print(f"SQL Query: {sql_query}")
        cursor.close()

        print("Dictionary is empty:", tables_data)

    def main(self):
        """Main function to execute the data import process."""
        try:
            connection = self.create_connection()
            self.create_table(connection)
            data: dict = self.parsed_data_from_file(file_path=self.log_file_path)
            self.table_filling(connection, tables_data=data)
        except TypeError as e:
            print(e)


if __name__ == '__main__':
    mfp = MSQFileParsed()
    mfp.main()