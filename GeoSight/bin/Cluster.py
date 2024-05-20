from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Processor import ElevationDataProcessor
from GeoSight.core.Clustering import  ClusterLabeling


  
def main():
    
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()


    

    processor = ElevationDataProcessor(elevation_data)
    #processor.find_best_parameters()
    
    processor.resample_elevation_data(scale_factor=0.01)  
    processor.fft_smooth(cutoff_frequency=60)  
    
    processor.plot_residuals()

    resampled_data = processor.elevation_data

    cluster_labeling = ClusterLabeling(resampled_data)
    cluster_labels = cluster_labeling.cluster_elevation_data(n_clusters=5)
    cluster_labeling.visualize_clusters(cluster_labels)


if __name__ == "__main__":
    main()