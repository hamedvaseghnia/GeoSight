from GeoSight.elevation_data_manager import ElevationDataManager
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
        plt.show()
    


    def cluster_elevation_data(self, n_clusters=3):
        """
        Performs KMeans clustering on the elevation data.
        """
        flat_elevation_data = self.elevation_data.reshape(-1, 1)
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(flat_elevation_data)
        labels = kmeans.labels_.reshape(self.elevation_data.shape)
        return labels

    def visualize_clusters(self, labels):
        """
        Visualizes the clusters of the elevation data.
        """
        plt.imshow(labels, cmap='viridis')
        plt.colorbar()
        plt.title('Elevation Data Clusters')
        plt.show()



