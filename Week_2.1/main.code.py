# Do you think it is a good idea to put all the code in one file,
# in this particula case? You are working with a client and a server
# so it's probable that they will run on / be distributed on different
# machines...

import pandas as pd
import http.server
import socketserver

class WeatherDataHandler(http.server.SimpleHTTPRequestHandler):
    """
    A custom HTTP request handler for weather data.

    Args:
        *args: Variable-length arguments passed to the parent class.
        **kwargs: Keyword arguments passed to the parent class.
    """
    def __init__(self, *args, **kwargs):
        self.data_provider = DataProvider('data.csv')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """
        Handles HTTP GET requests.
        """
    
        if self.path.startswith('/data'):
            self.handle_data_request()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_data_request(self):
        # Good. Nice small and good readable method.
        """
        Handles data-specific HTTP requests.
        """
    
        try:
            if self.path == '/data/all':
                response_data = self.data_provider.get_data()
            elif self.path.startswith('/data/') and self.path.count('/') == 2:
                _, _, param = self.path.split('/')
                if param.isdigit():
                    response_data = self.data_provider.get_data_yearly(int(param))
                else:
                    raise ValueError("Invalid year parameter")
            elif self.path.startswith('/data/') and self.path.count('/') == 3:
                _, _, from_year, to_year = self.path.split('/')
                if from_year.isdigit() and to_year.isdigit():
                    response_data = self.data_provider.get_data_by_range(int(from_year), int(to_year))
                else:
                    raise ValueError("Invalid year range parameters")
            else:
                raise ValueError("Invalid request")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response_data.encode())
        except ValueError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode())


class DataProvider:
    """
    A class for providing weather data.

    Args:
        csv_file (str): The path to the CSV file.
    """
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def get_data(self, range_of_years=None):
        """
        Retrieves weather data.

        Args:
            range_of_years (Union[int, list], optional): Range of years to retrieve the data for.
            If None, retrieves all data. If int, retrieves data for a specific year.
            If list, retrieves data for a range of years. Defaults to None.

        Returns:
            str: JSON-encoded weather data.
        """
        if range_of_years is None:
            return self.data.to_json(orient='records')
        elif isinstance(range_of_years, int):
            return self.get_data_yearly(range_of_years)
        elif isinstance(range_of_years, list) and len(range_of_years) == 2:
            return self.get_data_by_range(range_of_years[0], range_of_years[1])
        else:
            raise ValueError("Invalid parameter")

    # Good to have these small methods to return different data-sets. That makes 
    # your main code more manageble.
    def get_data_yearly(self, year):
        """
        Retrieves weather data for a specific year.

        Args:
            year (int): The year to retrieve the data for.

        Returns:
            str: JSON-encoded weather data for the specified year.
        """
        yearly_data = self.data[self.data['Year'] == year].transpose()
        yearly_data.columns = ['Value']
        return yearly_data.to_json()

    def get_data_by_range(self, from_year, to_year):
        """
        Retrieves weather data for a range of years.

        Args:
            from_year (int): The starting year of the range.
            to_year (int): The ending year of the range.

        Returns:
            str: JSON-encoded weather data for the specified year range.
        """
        data_by_range = self.data[(self.data['Year'] >= from_year) & (self.data['Year'] <= to_year)]
        return data_by_range.to_json(orient='records')


if __name__ == "__main__":
    PORT = 8080
    handler = WeatherDataHandler
    http = socketserver.TCPServer(("", PORT), handler)

    print("serving at port", PORT)
    http.serve_forever()

# Where's your client?
