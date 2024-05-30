from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Visualizer import ElevationDataVisualizer

def main():
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()

    # Get and print the coordinates of the corners
    corner_coordinates = data_manager.get_corner_coordinates()
    corner_names = ["Top Left", "Top Right", "Bottom Left", "Bottom Right"]
    for name, coords in zip(corner_names, corner_coordinates):
        print(f"{name}: {coords}")

    visualizer = ElevationDataVisualizer(elevation_data)
    visualizer.visualize_elevation_data()

if __name__ == "__main__":
    main()
