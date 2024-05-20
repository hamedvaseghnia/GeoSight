from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Visualizer import ElevationDataVisualizer

def main():
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()

    visualizer = ElevationDataVisualizer(elevation_data)
    visualizer.visualize_elevation_data()

if __name__ == "__main__":
    main()
