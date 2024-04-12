from module.elevation_data_manager import ElevationDataManager
import numpy as np
import matplotlib.pyplot as plt

class ElevationDataSlopeCalculator:
    """
    A class to calculate and visualize the slope from elevation data.
    """
    
    def __init__(self, elevation_data):
        """
        Initializes the calculator with loaded elevation data.
        
        Parameters:
        - elevation_data: Array-like, the elevation data to calculate slope from.
        """
        self.elevation_data = elevation_data

    def calculate_slope(self):
        """
        Calculates the slope from the elevation data.
        
        Returns:
        - slope_degrees: A 2D numpy array of the slope in degrees.
        """
        gradient_x, gradient_y = np.gradient(self.elevation_data)
        slope = np.sqrt(gradient_x**2 + gradient_y**2)
        slope_degrees = np.arctan(slope) * (180 / np.pi)
        return slope_degrees
    
    def visualize_slope(self, slope_degrees):
        """
        Visualizes the calculated slope in degrees using a matplotlib plot.
        
        Parameters:
        - slope_degrees: A 2D numpy array of the slope in degrees.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        slope_mappable = ax.imshow(slope_degrees, cmap='pink', aspect='auto')
        plt.colorbar(slope_mappable, label='Slope (degrees)')
        plt.show()


