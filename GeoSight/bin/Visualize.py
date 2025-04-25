from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Visualizer import ElevationDataVisualizer

def main():
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()
    corner_coordinates = data_manager.get_corner_coordinates()

    visualizer = ElevationDataVisualizer(elevation_data)

    # Save the satellite image using real-world coordinates
    visualizer.save_satellite_image(corner_coordinates)

    # Show elevation plot and enable point selection
    visualizer.visualize_elevation_data()

if __name__ == "__main__":
    main()
