from module.elevation_data_manager import ElevationDataManager
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class ClusterLabeling:
    """
    A class to calculate and visualize the slope from elevation data.
    """
    
    def __init__(self, elevation_data):
        """
        Initializes the calculator with loaded elevation data.
        """
        self.elevation_data = elevation_data

 
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
        plt.imshow(labels, cmap='jet')
        plt.colorbar()
        plt.show()



