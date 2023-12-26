import os
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
from os import listdir, makedirs
from os.path import join, splitext, exists
import numpy as np


class graph_gen_and_saving:
    def __init__(self, data_dir="working_data/", file_extension=".txt", output_dir="graphs/", control_file="norm.txt"):
        self.data_dir = data_dir
        self.file_extension = file_extension
        self.output_dir = output_dir
        self.control_file = control_file
        self.labels = ["Pre-Cycling", "ON (Cycling)", "OFF (Cycling)", "Post-Cycling"]
        self.colors = {"Pre-Cycling": "blue", "ON (Cycling)": "green", "OFF (Cycling)": "red", "Post-Cycling": "purple"}
        makedirs(self.output_dir, exist_ok=True)

    def list_files(self):
        return [f for f in listdir(self.data_dir) if f.endswith(self.file_extension)]

    def read_data(self, file_name):
        file_path = join(self.data_dir, file_name)
        try:
            return read_csv(file_path, header=1)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except pd.errors.EmptyDataError:
            print(f"No data in file: {file_path}")
            return None

    def normalize_data(self, data, control_mean, control_std):
        if control_std == 0:
            print("Standard deviation is zero, normalization not possible.")
            return None
        return (data - control_mean) / control_std

    def process_all_files(self, norm=True):
        if not exists(join(self.data_dir, self.control_file)):
            print(f"Control file not found: {self.control_file}")
            return {}

        control_data = self.read_data(self.control_file)
        if control_data is None:
            return {}

        control_mean = np.mean(control_data.iloc[:, 1])
        control_std = np.std(control_data.iloc[:, 1])

        files = self.list_files()

        normalized_data = {}
        for file in files:
            if file != self.control_file:
                file_data = self.read_data(file)
                if file_data is not None:
                    if norm:
                        file_data.iloc[:, 1] = self.normalize_data(file_data.iloc[:, 1], control_mean, control_std)
                    else:
                        file_data.iloc[:, 1] = file_data.iloc[:, 1];
                    normalized_data[file] = file_data
        return normalized_data

    def plot_and_save_graphs(self, data):
        """Generate and save scatter plots for each file, checking for label substrings."""
        for file, df in data.items():
            if df is not None:
                plt.figure()
                for label_key in self.labels:
                    # Filter data where the actual label contains the label_key as a substring
                    # Use regex=False to treat the label_key as a literal string
                    filtered_data = df[df.iloc[:, 3].str.contains(label_key, regex=False)]
                    if not filtered_data.empty:
                        plt.scatter(filtered_data.iloc[:, 0], filtered_data.iloc[:, 1],
                                    color=self.colors.get(label_key, "black"), label=label_key)
                plt.title(file)
                plt.xlabel('X Axis')  # Replace with your actual x-axis label
                plt.ylabel('Normalized Value')
                plt.legend()
                output_file = join(self.output_dir, f"{splitext(file)[0]}.png")
                plt.savefig(output_file)
                plt.close()


if __name__ == "__main__":
    processor = graph_gen_and_saving()
    normalized_data = processor.process_all_files()
    processor.plot_and_save_graphs(normalized_data)
