import matplotlib.pyplot as plt
import pandas as pd
from create_data_from_table_data import MSQFileParsed
from parsed_data_from_log import Graph
from mysql.connector import Error
from matplotlib.ticker import FuncFormatter
from datetime import datetime

class Charts(MSQFileParsed, Graph):
    """Class for creating and displaying multiple charts on a single sheet using Matplotlib and Pandas."""

    def __init__(self) -> None:
        """Initialize the Charts object."""
        super().__init()

    def get_values(self, connection) -> pd.DataFrame:
        """Get data from the MySQL database and return it as a Pandas DataFrame."""
        try:
            cursor = connection.cursor()
            sql_query = f"SELECT * FROM {self.table_name}"
            cursor.execute(sql_query)

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            df = pd.DataFrame(rows, columns=columns)

            return df

        except Error as err:
            print(f"MySQL Connector Error: {err}")
            return pd.DataFrame()
        
    def format_time_ticks(self, x, _):
        """Format the x-axis tick labels with human-readable date and time."""
        timestamp = int(x)
        dt_object = datetime.utcfromtimestamp(timestamp / 1e9)  # assuming time is in nanoseconds
        return f"{dt_object:%Y-%m-%d %H:%M:%S}"

    def create_charts(self, df: pd.DataFrame):
        """Create and display multiple charts based on the data in the DataFrame."""
        print(f"{df} \n")
        try:
            # Convert string values to integers
            columns_to_plot = ['decodedframes', 'lossframe', 'losspacket',]
            for column_name in columns_to_plot:
                if column_name in df.columns:
                    df[column_name] = df[column_name].astype(int)
                else:
                    print(f"Column '{column_name}' not found in DataFrame.")
                    return

            fig, axes = plt.subplots(nrows=len(columns_to_plot), sharex=True, figsize=(15, 10))
            for i, column_name in enumerate(columns_to_plot):
                # Plot with a blue solid line and circles for each data point
                axes[i].plot(df['time'], df[column_name], label=column_name, linewidth=0.5, markersize=6)

                # Set the title and labels
                axes[i].set_title(f"Chart: {column_name}", fontsize=16)
                axes[i].set_ylabel(f"{column_name}", fontsize=14)
                axes[i].grid(True, linestyle='--', alpha=0.7)

            # Increase spacing between x-axis labels
            plt.subplots_adjust(hspace=0.5)

            fig.suptitle("Multiple Charts on One Sheet", fontsize=20)
            plt.xlabel("Time", fontsize=14)

            # Add legend with a custom location
            axes[0].legend(loc='upper left', fontsize='small')

            for ax in axes:
                ax.grid(True, linestyle='--', alpha=0.7)

            plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
            axes[-1].xaxis.set_major_locator(plt.MaxNLocator(8)) 
            #axes[-1].xaxis.set_major_formatter(FuncFormatter(self.format_time_ticks))

            plt.tight_layout()
            plt.show()
        except TypeError as e:
            print(e)
    
    def create_csv_file(self, df: pd.DataFrame, filename):
        """Create 'scv' file from table data"""
        try:
            # Customize your columns if needed
            columns_to_select = ['time', 'decodedframes', 'lossframe', 'losspacket']

            if all(column in df.columns for column in columns_to_select):
                selected_df = df[columns_to_select]
                selected_df.to_csv(filename, index=False)
                print(f"CSV file '{filename}' created successfully.")
            else:
                print("Not all specified columns are present in the DataFrame.")
        except Exception as e:
            print(f"Error creating CSV file: {e}")


    def main(self):
        """Main function to execute the data import and chart creation process."""
        connection = self.create_connection()
        df_main = self.get_values(connection)
        self.create_csv_file(df=df_main,filename="selected_data.csv")
        self.create_charts(df=df_main)

if __name__ == '__main__':
    chrt = Charts()
    chrt.main()