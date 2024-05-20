import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from GeoSight.core.elevation_data_manager import ElevationDataManager

class TestElevationDataManager(unittest.TestCase):
    @patch('GeoSight.core.elevation_data_manager.rasterio.open')
    @patch('GeoSight.core.elevation_data_manager.resources.files')
    def test_load_elevation_data(self, mock_files, mock_open):
        # Set up
        mock_files.return_value.joinpath.return_value = 'fake_data_path'
        mock_src = MagicMock()
        mock_src.read.return_value = np.array([[1, 2], [3, 4]])  # Example data
        mock_open.return_value.__enter__.return_value = mock_src

        # Create an instance of ElevationDataManager
        manager = ElevationDataManager()

        # Call the method to load elevation data
        result = manager.load_elevation_data()

        # Assert that the method returned the expected result
        np.testing.assert_array_equal(result, np.array([[1, 2], [3, 4]]))

        # Assert that the rasterio.open method was called with the correct path
        mock_files.assert_called_once_with('Data')
        mock_files.return_value.joinpath.assert_called_once_with('image.tif')
        mock_open.assert_called_once_with('fake_data_path')

if __name__ == '__main__':
    unittest.main()
