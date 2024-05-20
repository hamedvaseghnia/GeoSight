import rasterio
import gdown
import os
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

class ElevationDataVisualizer:
    """
    A class to visualize elevation data.
    """
    def __init__(self, elevation_data):
        """
        Initializes the visualizer with loaded elevation data.
        
        Parameters:
        - elevation_data: Array-like, the elevation data to visualize.
        """
        self.elevation_data = elevation_data

    def visualize_elevation_data(self):
        """
        Visualizes the loaded elevation data using a terrain color map.
        """
        _, ax = plt.subplots(figsize=(10, 6))
        mappable = ax.imshow(self.elevation_data, cmap='terrain')
        plt.colorbar(mappable, label='Elevation (m)')
        plt.show()

def main():
    url = "https://drive.google.com/uc?id=1g_E1DW1eZ1yUytz8PSpLoQNzsmA9rdGZ"
    output_path = "examples/image.tif"
    
    data_manager = ElevationDataManager()
    
    # Check if the file exists; if not, download it
    if not os.path.exists(output_path):
        data_manager.download_elevation_data(url, output_path)
    
    # Load the elevation data
    elevation_data = data_manager.load_elevation_data(output_path)
    
    # Create an instance of ElevationDataVisualizer
    visualizer = ElevationDataVisualizer(elevation_data)
    
    # Visualize the elevation data
    visualizer.visualize_elevation_data()

if __name__ == "__main__":
    main()
