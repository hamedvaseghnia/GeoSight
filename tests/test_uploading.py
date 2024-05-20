import unittest
import os
import numpy as np
from GeoSight.core.elevation_data_manager import ElevationDataManager

class TestElevationDataManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestElevationDataManager, cls).setUpClass()
        # Save the original working directory to restore it later
        cls.original_working_dir = os.getcwd()

    @classmethod
    def tearDownClass(cls):
        # Restore the original working directory after tests
        os.chdir(cls.original_working_dir)
        super(TestElevationDataManager, cls).tearDownClass()

    def test_load_elevation_data(self):
        """Test if elevation data loads correctly from a GeoTIFF file."""
        # Change the working directory to the project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        os.chdir(project_root)
        
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
