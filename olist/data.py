from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.

    Methods:
        get_data():
            Loads and returns a dictionary where keys are dataset names (e.g., 'sellers', 'orders')
            and values are pandas DataFrames loaded from corresponding CSV files.

        ping():
            Prints "pong" to confirm the method is callable.
    """
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        csv_path = Path("~/.workintech/olist/data/csv").expanduser()

        file_paths = list(csv_path.glob("*.csv"))

        # csv dizinindeki dosya adlarını içeren file_names listesi
        file_names = []
        for path in file_paths:
            file_names.append(path.name)

        # key_names oluşturma
        key_names = [
            name.replace("olist_","")
            .replace("_dataset.csv","")
            .replace(".csv","")
            for name in file_names
            ]

        # data sözlüğünü oluşturma
        data = {}
        for key, file in zip(key_names, file_names):
            df = pd.read_csv(csv_path / file)
            data[key] = df

        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
