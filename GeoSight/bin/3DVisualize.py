from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Processor import ElevationDataProcessor


  
def main():
    
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()

    processor = ElevationDataProcessor(elevation_data)
    processor.resample_elevation_data(scale_factor=0.01)  
    processor.fft_smooth(cutoff_frequency=60)  
    processor.visualize_smoothed_data()
   

if __name__ == "__main__":
    main()