import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from GeoSight.core.Visualizer import ElevationDataVisualizer

class TestElevationDataVisualizer(unittest.TestCase):
    def setUp(self):
        self.elevation_data = np.random.rand(10, 10)

    def test_init(self):
        visualizer = ElevationDataVisualizer(self.elevation_data)
        self.assertIsNotNone(visualizer)
        self.assertEqual(visualizer.elevation_data.shape, self.elevation_data.shape)

    @patch('GeoSight.core.Visualizer.plt')
    def test_visualize_elevation_data(self, mock_plt):
        visualizer = ElevationDataVisualizer(self.elevation_data)
        
        # Create a mock axis object
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (None, mock_ax)
        
        # Call the method
        visualizer.visualize_elevation_data()
        
        # Assert that plt.subplots and ax.imshow were called
        mock_plt.subplots.assert_called_once()
        mock_ax.imshow.assert_called_once_with(self.elevation_data, cmap='terrain')

if __name__ == '__main__':
    unittest.main()
