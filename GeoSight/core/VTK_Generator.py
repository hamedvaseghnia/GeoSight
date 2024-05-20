# vtk_exporter.py
import numpy as np
import pyvista as pv

class VTKExporter:
    def __init__(self, smoothed_data):
        self.smoothed_data = smoothed_data

    def export_to_vtk(self, filename):
        """
        Exports the smoothed elevation data to a VTK ASCII file as a 3D structured grid.
        """
        if self.smoothed_data is None:
            raise ValueError("Smoothed data is not available. Please run fft_smooth first.")
        
        # Define the number of points along each dimension
        nx, ny = self.smoothed_data.shape
        nz = 1  # Elevation will now be used to modify Z-coordinates, creating a 3D surface
        
        # Create a meshgrid for X, Y coordinates
        x_km = np.linspace(0, nx-1, nx)
        y_km = np.linspace(0, ny-1, ny)

        x = x_km * 100
        y = y_km * 100
        z = np.zeros((nx, ny))  # Initialize Z as a flat surface
        X, Y = np.meshgrid(x, y, indexing='ij')
        
        # Use elevation data as Z-coordinates to create a 3D surface
        Z = self.smoothed_data
        
        # Stack the X, Y, and now Z (elevation data) to create 3D points
        points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
        
        # Create the structured grid
        grid = pv.StructuredGrid()
        grid.points = points
        # The dimensions must account for the single layer of points in Z; thus, nz is 2 to form a valid volume
        grid.dimensions = [nx, ny, nz]
        
        # You can still attach the elevation data as scalar point data if needed
        grid.point_data["elevation"] = Z.flatten(order='C')  # Ensure correct ordering
        
        # Save the grid to a VTK file in ASCII format
        grid.save(filename, binary=False)
        
        print(f"Exported 3D structured grid to {filename} in ASCII format.")
