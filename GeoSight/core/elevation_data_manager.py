import rasterio
from importlib import resources
from rasterio.warp import transform

class ElevationDataManager:
    def __init__(self):
        self.elevation_data = None
        self.transform = None
        self.crs = None

    def load_elevation_data(self):
        """
        Loads elevation data from the TIFF file using importlib resources to access the package resource.
        """
        data_path = resources.files('Data').joinpath('image.tif')
        with rasterio.open(data_path) as src:
            self.elevation_data = src.read(1)
            self.transform = src.transform
            self.crs = src.crs
        return self.elevation_data

    def get_corner_coordinates(self):
        """
        Returns the geographic coordinates of the four corners of the TIFF file.
        """
        if self.transform is None or self.crs is None:
            raise ValueError("Elevation data must be loaded before getting coordinates.")

        # Get dimensions
        height, width = self.elevation_data.shape

        # Calculate pixel coordinates of the corners
        corners = [(0, 0), (width, 0), (0, height), (width, height)]
        coords = [self.transform * corner for corner in corners]

        # Check if the CRS is geographic (longitude, latitude) or projected
        if self.crs.is_geographic:
            return coords  # Already in geographic coordinates
        else:
            # If projected, transform to geographic coordinates (longitude, latitude)
            lons, lats = transform(self.crs, rasterio.crs.CRS.from_epsg(4326), *zip(*coords))
            return list(zip(lons, lats))

