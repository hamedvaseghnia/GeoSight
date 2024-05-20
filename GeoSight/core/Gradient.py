from GeoSight.core.elevation_data_manager import ElevationDataManager
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

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
        Visualizes the clusters of the elevation data.
        """
        plt.imshow(slope_degrees, cmap='viridis')
        plt.colorbar()
        plt.savefig('GeoSight/output/Slope_plot.png')
        plt.show()

    



        



