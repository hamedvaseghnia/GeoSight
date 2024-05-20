import rasterio
import gdown
import os
import numpy as np
import matplotlib.pyplot as plt

class ElevationDataManager:
    def __init__(self):
        self.elevation_data = None

    def download_elevation_data(self, url, output_path):
        """
        Downloads the elevation data from the given URL to the specified output path.
        """
        gdown.download(url, output_path, quiet=False)

    def load_elevation_data(self, file_path):
        """
        Loads elevation data from the TIFF file.
        """
        with rasterio.open(file_path) as src:
            self.elevation_data = src.read(1)
        return self.elevation_data

class ElevationDataSlopeCalculator:
    """
    A class to calculate and visualize the slope from elevation data.
    """
    
    def __init__(self, elevation_data):
        """
        Initializes the calculator with loaded elevation data.
        """
        self.elevation_data = elevation_data

    def calculate_slope(self):
        """
        Calculates the slope from the elevation data.
        """
        gradient_x, gradient_y = np.gradient(self.elevation_data)
        slope = np.sqrt(gradient_x**2 + gradient_y**2)
        slope_degrees = np.arctan(slope) * (180 / np.pi)
        return slope_degrees
    
    def visualize_slope(self, slope_degrees):
        """
        Visualizes the slope of the elevation data.
        """
        plt.imshow(slope_degrees, cmap='viridis')
        plt.colorbar(label='Slope (degrees)')
        plt.savefig('Slope_plot.png')
        plt.show()

def main():
    # Define the URL and output path
    url = "https://drive.google.com/uc?id=1g_E1DW1eZ1yUytz8PSpLoQNzsmA9rdGZ"
    output_path = "examples/image.tif"
    
    # Create an instance of ElevationDataManager
    data_manager = ElevationDataManager()
    
    # Check if the file exists; if not, download it
    if not os.path.exists(output_path):
        data_manager.download_elevation_data(url, output_path)
    
    # Load the elevation data
    elevation_data = data_manager.load_elevation_data(output_path)
    
    # Create an instance of ElevationDataSlopeCalculator
    slope_calculator = ElevationDataSlopeCalculator(elevation_data)
    
    # Calculate the slope
    slope_degrees = slope_calculator.calculate_slope()
    
    # Visualize the slope
    slope_calculator.visualize_slope(slope_degrees)

if __name__ == "__main__":
    main()
