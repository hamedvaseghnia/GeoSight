import unittest
from module.elevation_data_manager import ElevationDataManager
import numpy as np

class TestElevationDataManager(unittest.TestCase):
    def test_load_elevation_data(self):
        """Test if elevation data loads correctly from a GeoTIFF file."""
        manager = ElevationDataManager()
        elevation_data = manager.load_elevation_data()

        # Assert that the result is not None
        self.assertIsNotNone(elevation_data, "Elevation data should not be None after loading.")

        # Assert that the result is a numpy array
        self.assertIsInstance(elevation_data, np.ndarray, "Loaded elevation data should be a numpy array.")
        self.assertGreater(elevation_data.size, 0, "Elevation data array should not be empty.")
        self.assertGreater(elevation_data.shape[0], 0, "Elevation data should have positive height.")
        self.assertGreater(elevation_data.shape[1], 0, "Elevation data should have positive width.")

if __name__ == '__main__':
    unittest.main()
