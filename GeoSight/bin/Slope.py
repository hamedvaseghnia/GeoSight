from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Gradient import ElevationDataSlopeCalculator

def main():
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()

    slope_calculator = ElevationDataSlopeCalculator(elevation_data)
    slope_degrees = slope_calculator.calculate_slope()
    slope_calculator.visualize_slope(slope_degrees)

if __name__ == "__main__":
    main()