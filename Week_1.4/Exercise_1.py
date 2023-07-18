import csv
import json
import linecache
import time
import matplotlib.pyplot as plt

class CsvConverter:
    def __init__(self, csv_file):
        """
        Initializes a CsvConverter instance.

        Args:
            csv_file (str): The path to the CSV file.
        """
        self.csv_file = csv_file
        self.header = linecache.getline(self.csv_file, 1).strip('\n').split(',')

    def csv_to_json(self, list_lines):
        """
        Converts a list of CSV lines to a JSON string.

        Args:
            list_lines (list): List of CSV lines.

        Returns:
            str: JSON string representation of the CSV data.
        """
        output = [
            dict(zip(self.header, line.strip().split(',')))
            for line in list_lines
            if len(line.strip().split(',')) == len(self.header)
        ]
        return json.dumps(output)

    def __str__(self):
        """
        Returns a string representation of the CsvConverter object.

        Returns:
            str: The string representation.
        """
        return f'CSV file: {self.csv_file}'


class Reader:
    def __init__(self, csv_file='dSST.csv', stride=5):
        """
        Initializes a Reader instance.

        Args:
            csv_file (str): The path to the CSV file.
            stride (int): The number of lines to read in each iteration.
        """
        self.csv_file = csv_file
        self.stride = stride
        self.header_line = linecache.getline(self.csv_file, 1).strip('\n').split(',')
        self.current_line = 2  # Start from line 2 (excluding the header line)
        self.observers = set()

    def add_observer(self, observer):
        """
        Adds an observer to the Reader.

        Args:
            observer (object): The observer object to add.
        """
        self.observers.add(observer)

    def remove_observer(self, observer):
        """
        Removes an observer from the Reader.

        Args:
            observer (object): The observer object to remove.
        """
        self.observers.discard(observer)

    def notify_observers(self, data):
        """
        Notifies all observers with the provided data.

        Args:
            data (list): The data to notify the observers with.
        """
        _ = [observer.update(data) for observer in self.observers]

    def get_lines(self):
        """
        Retrieves the lines from the CSV file.

        Returns:
            list: The parsed data as a list of dictionaries.
        """
        line_lists = [
            linecache.getline(self.csv_file, self.current_line + i)
            for i in range(self.stride)
            if linecache.getline(self.csv_file, self.current_line + i).strip() != ''
        ]

        if line_lists:
            output = CsvConverter(self.csv_file).csv_to_json(line_lists)
            self.current_line += self.stride

            # Parse the JSON data
            parsed_data = json.loads(output)

            # Notify observers with the new data
            self.notify_observers(parsed_data)
            return parsed_data
        else:
            return []

    def run(self):
        """
        Starts the Reader and continuously reads lines from the CSV file.
        """
        while True:
            json_data = self.get_lines()
            if json_data == '':
                break
            time.sleep(5)


class AverageYear:
    def __init__(self):
        """
        Initializes an AverageYear instance.
        """
        self.years = []
        self.temperatures = []
        self.figure, self.ax = plt.subplots()

    def update(self, data):
        """
        Updates the AverageYear instance with new data.

        Args:
            data (list): The new data to update the instance with.
        """
        if not data:
            return

        avg = self.calculate_average_temperature(data)
        if avg:
            year = len(self.years) + 1
            self.years.append(year)
            self.temperatures.append(avg)
            self.plot_average_temperature()

    def calculate_average_temperature(self, data):
        """
        Calculates the average temperature from the provided data.

        Args:
            data (list): The data to calculate the average temperature from.

        Returns:
            float: The average temperature.
        """
        count = len(data)
        sum_temp = sum(float(line['J-D']) for line in data)
        if count == 0:
            return None
        avg = sum_temp / count
        return avg

    def plot_average_temperature(self):
        """
        Plots the average temperature over the years.
        """
        self.ax.clear()
        self.ax.plot(self.years, self.temperatures, 'bo-')
        self.ax.set_xlabel('Year')
        self.ax.set_ylabel('Average Temperature')
        self.ax.set_title('Average Yearly Temperature')
        self.ax.grid(True)
        self.figure.savefig('average_yearly_temperature.png')  # Save the figure as a PNG file


class AverageMonth:
    def __init__(self):
        """
        Initializes an AverageMonth instance.
        """
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.monthly_averages = {month: [] for month in self.months}
        self.years = []
        self.yearly_averages = []
        self.monthly_figure, self.monthly_ax = plt.subplots()
        self.yearly_figure, self.yearly_ax = plt.subplots()

    def update(self, data):
        """
        Updates the AverageMonth instance with new data.

        Args:
            data (list): The new data to update the instance with.
        """
        self.calculate_average_temperature(data)
        self.plot_average_monthly_temperature()
        self.plot_average_yearly_temperature()

    def calculate_average_temperature(self, data):
        """
        Calculates the average temperature from the provided data.

        Args:
            data (list): The data to calculate the average temperature from.
        """
        count = len(data)
        sum_temp = sum(float(line['J-D']) for line in data)
        if count == 0:
            return None
        avg = sum_temp / count
        self.years.append(len(self.years) + 1)
        self.yearly_averages.append(avg)
        self.monthly_averages = {month: [float(data[0][month]) for _ in range(len(data))] for month in self.months}

    def plot_average_monthly_temperature(self):
        """
        Plots the average monthly temperatures.
        """
        self.monthly_ax.clear()
        [self.monthly_ax.plot(range(1, len(temps) + 1), temps, label=month) for month, temps in self.monthly_averages.items()]

        self.monthly_ax.set_xlabel('Data Point')
        self.monthly_ax.set_ylabel('Average Temperature')
        self.monthly_ax.set_title('Average Monthly Temperatures')
        self.monthly_ax.legend()
        self.monthly_ax.grid(True)
        self.monthly_figure.savefig('average_monthly_temperatures.png')  # Save the figure as a PNG file

    def plot_average_yearly_temperature(self):
        """
        Plots the average yearly temperature.
        """
        self.yearly_ax.clear()
        self.yearly_ax.plot(self.years, self.yearly_averages, 'bo-')
        self.yearly_ax.set_xlabel('Year')
        self.yearly_ax.set_ylabel('Average Temperature')
        self.yearly_ax.set_title('Average Yearly Temperature')
        self.yearly_ax.grid(True)
        self.yearly_figure.savefig('average_yearly_temperature.png')  # Save the figure as a PNG file


# Usage example
reader = Reader('dSST.csv')
average_year = AverageYear()
average_month = AverageMonth()
reader.add_observer(average_year)
reader.add_observer(average_month)
reader.run()
