import pyvista
from PVGeo.grids import ExtractTopography
from PVGeo.model_build import CreateTensorMesh

class TopographyExtractor:
    def __init__(self, origin, xcellstr, ycellstr, zcellstr, file_path):
        self.origin = origin
        self.xcellstr = xcellstr
        self.ycellstr = ycellstr
        self.zcellstr = zcellstr
        self.file_path = file_path
        self.mesh = None
        self.topo = None
    
    def create_tensor_mesh(self):
        self.mesh = CreateTensorMesh(
            origin=self.origin,
            xcellstr=self.xcellstr,
            ycellstr=self.ycellstr,
            zcellstr=self.zcellstr,
        ).apply()

    def read_topography(self):
        self.topo = pyvista.read(self.file_path)
    
    def extract_and_display_topography(self, tolerance=100.0, remove=True, show_edges=True):
        if self.mesh is None or self.topo is None:
            print("Mesh or topography data is missing.")
            return
        
        p = pyvista.Plotter()
        p.add_mesh(self.topo, cmap="terrain")
        
        if remove:
            extracted = ExtractTopography(tolerance=tolerance, remove=remove).apply(self.mesh, self.topo)
            p.add_mesh(extracted, color=True, show_edges=show_edges, opacity=0.1)
        else:
            extracted = ExtractTopography().apply(self.mesh, self.topo)
            threshed = extracted.threshold(0.5, scalars="Extracted")
            p.add_mesh(threshed, color=True, show_edges=show_edges)
        
        #p.show_grid()
        p.show()
        extracted.save('GeoSight/output/Cell_Data.vtk')