import unittest
from unittest.mock import patch, MagicMock
import pyvista
from PVGeo.grids import ExtractTopography
from PVGeo.model_build import CreateTensorMesh
from GeoSight.core.PVGeo import TopographyExtractor  


class TestTopographyExtractor(unittest.TestCase):
    def setUp(self):
        self.origin = (0, 0, 0)
        self.xcellstr = '1 2 3'
        self.ycellstr = '1 2 3'
        self.zcellstr = '1 2 3'
        self.file_path = 'fake_path.vtk'
        self.extractor = TopographyExtractor(
            origin=self.origin,
            xcellstr=self.xcellstr,
            ycellstr=self.ycellstr,
            zcellstr=self.zcellstr,
            file_path=self.file_path
        )

    @patch('PVGeo.model_build.CreateTensorMesh.apply', return_value='mock_mesh')
    def test_create_tensor_mesh(self, mock_create_tensor_mesh):
        self.extractor.create_tensor_mesh()
        mock_create_tensor_mesh.assert_called_once()
        self.assertEqual(self.extractor.mesh, 'mock_mesh')

    @patch('pyvista.read', return_value='mock_topo')
    def test_read_topography(self, mock_pyvista_read):
        self.extractor.read_topography()
        mock_pyvista_read.assert_called_once_with(self.file_path)
        self.assertEqual(self.extractor.topo, 'mock_topo')

    @patch('pyvista.Plotter')
    @patch('PVGeo.grids.ExtractTopography.apply', return_value=MagicMock(save=MagicMock()))
    def test_extract_and_display_topography_remove_true(self, mock_extract_topography, mock_pyvista_plotter):
        self.extractor.mesh = 'mock_mesh'
        self.extractor.topo = 'mock_topo'
        mock_plotter_instance = mock_pyvista_plotter.return_value

        self.extractor.extract_and_display_topography(remove=True)
        
        mock_extract_topography.assert_called_once_with(self.extractor.mesh, self.extractor.topo)
        mock_plotter_instance.add_mesh.assert_any_call('mock_topo', cmap='terrain')
        mock_plotter_instance.add_mesh.assert_any_call(mock_extract_topography.return_value, color=True, show_edges=True, opacity=0.1)
        mock_plotter_instance.show.assert_called_once()
        mock_extract_topography.return_value.save.assert_called_once_with('GeoSight/output/Cell_Data.vtk')

    @patch('pyvista.Plotter')
    @patch('PVGeo.grids.ExtractTopography.apply', return_value=MagicMock(threshold=MagicMock(return_value='mock_threshed')))
    def test_extract_and_display_topography_remove_false(self, mock_extract_topography, mock_pyvista_plotter):
        self.extractor.mesh = 'mock_mesh'
        self.extractor.topo = 'mock_topo'
        mock_plotter_instance = mock_pyvista_plotter.return_value

        self.extractor.extract_and_display_topography(remove=False)
        
        mock_extract_topography.assert_called_once_with(self.extractor.mesh, self.extractor.topo)
        extracted_mock = mock_extract_topography.return_value
        extracted_mock.threshold.assert_called_once_with(0.5, scalars="Extracted")
        mock_plotter_instance.add_mesh.assert_any_call('mock_topo', cmap='terrain')
        mock_plotter_instance.add_mesh.assert_any_call('mock_threshed', color=True, show_edges=True)
        mock_plotter_instance.show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
