import rasterio
from importlib import resources

class ElevationDataManager:
    def __init__(self):
        self.elevation_data = None

    def load_elevation_data(self):
        """
        Loads elevation data from the TIFF file
        """
        data_path = resources.files('module.data').joinpath('image.tif')
        with rasterio.open(data_path) as src:
            self.elevation_data = src.read(1)
        return self.elevation_data
