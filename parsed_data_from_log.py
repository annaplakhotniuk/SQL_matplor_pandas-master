import re
import matplotlib.pyplot as plt

class Graph:
    """Class for parsing log data and creating charts."""

    file_path = 'bstr_client.log'
    find_key_word = "SStat:"

    def __init__(self) -> None:
        """Initialize the Graph object."""
        self.charts_data: dict = {
            'decodedFrames': [],
            'lossFrame': [],
            'lossPacket': [],
            'realFrames': [],
            'receivedFrames': [],
            'time': []
        }

    def parsed_data_from_file(self, file_path=file_path, find_key_word=find_key_word) -> dict:
        """Parse data from a log file and store it in self.charts_data."""
        with open(file_path, mode='r', encoding='UTF-8') as file:
            lines = file.readlines()
            for line in lines:
                if find_key_word in line:
                    pattern = r'"(.*?)":\s*("[^"]*"|\d+)'
                    match = re.findall(pattern, line)
                    temporary = {}
                    for key, value in match:
                        if key in self.charts_data.keys():
                            temporary[key] = int(value)
                            self.charts_data[key].append(temporary[key])
            
            return self.charts_data

    def charts_adjusts(self):
        """Create and display charts based on data in self.charts_data."""
        fig, ax = plt.subplots()
        
        for key, values in self.charts_data.items():
            ax.plot(values, label=key, linewidth=3)

        ax.set_title("Session Params", fontsize=24)
        ax.set_xlabel("Time", fontsize=24)
        ax.set_ylabel("Value", fontsize=24)
        ax.tick_params(axis='both', labelsize=24)
        ax.legend()  # Add a legend for the keys
        plt.show()