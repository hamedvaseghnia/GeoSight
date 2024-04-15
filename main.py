from GeoSight.elevation_data_manager import ElevationDataManager
from GeoSight.Processor import ElevationDataProcessor
from GeoSight.Visualizer import ElevationDataVisualizer
from GeoSight.Gradient import ElevationDataSlopeCalculator
from GeoSight.PVGeo import TopographyExtractor
from GeoSight.Clustering import  ClusterLabeling

  
def main():
    
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()

    visualizer = ElevationDataVisualizer(elevation_data)
    visualizer.visualize_elevation_data()

    slope_calculator = ElevationDataSlopeCalculator(elevation_data)
    slope_degrees = slope_calculator.calculate_slope()
    slope_calculator.visualize_slope(slope_degrees)


    cluster_labeling = ClusterLabeling(elevation_data)
    cluster_labels = cluster_labeling.cluster_elevation_data(n_clusters=5)
    cluster_labeling.visualize_clusters(cluster_labels)


    processor = ElevationDataProcessor(elevation_data)
    processor.resample_elevation_data(scale_factor=0.01)  
    processor.fft_smooth(cutoff_frequency=30)  
    #processor.visualize_smoothed_data()
    processor.export_to_vtk("topo_mapp.vtk")


    topo_extractor = TopographyExtractor(
        origin=[0, 0, 2000],
        xcellstr="1000 500 50*250 500 1000",
        ycellstr="1000 500 55*250 500 1000",
        zcellstr="30*100.0 5*500.0 500",
        file_path="topo_mapp.vtk",
    )
    topo_extractor.create_tensor_mesh()
    topo_extractor.read_topography()
    topo_extractor.extract_and_display_topography()

if __name__ == "__main__":
    main()