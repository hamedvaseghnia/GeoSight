# This file does something.
import matplotlib.pyplot as plt 

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
        plt.savefig('GeoSight/output/Elevation_plot.png')
        plt.show()
