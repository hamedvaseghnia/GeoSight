from GeoSight.core.elevation_data_manager import ElevationDataManager
from GeoSight.core.Processor import ElevationDataProcessor
from GeoSight.core.PVGeo import TopographyExtractor
from GeoSight.core.VTK_Generator import  VTKExporter

  
def main():
    
    data_manager = ElevationDataManager()
    elevation_data = data_manager.load_elevation_data()

    processor = ElevationDataProcessor(elevation_data)
    processor.resample_elevation_data(scale_factor=0.01)  
    processor.fft_smooth(cutoff_frequency=60)  
  

    vtk_exporter = VTKExporter(processor.smoothed_data)
    vtk_exporter.export_to_vtk("topo_mapp.vtk")

    topo_extractor = TopographyExtractor(
        origin=[0, 0, 2000],
        xcellstr="1000 500 50*250 500 1000",
        ycellstr="1000 500 55*250 500 1000",
        zcellstr="30*100.0 5*500.0 500",
        file_path="topo_mapp.vtk",
    )
    topo_extractor.create_tensor_mesh()
    topo_extractor.read_topography()
    topo_extractor.extract_and_display_topography()

if __name__ == "__main__":
    main()