
import numpy as np
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import zoom
import pyvista as pv

class ElevationDataProcessor:
    """
    Adjusted to accept elevation data directly, not a file path.
    """
    def __init__(self, elevation_data):
        self.elevation_data = elevation_data
        self.smoothed_data = None
    
    def resample_elevation_data(self, scale_factor):
        """
        Resamples the elevation data based on the provided scale factor using SciPy's zoom function.
        
        Parameters:
        - scale_factor: Float, the factor by which to scale the elevation data's resolution.
        """
        # Ensure elevation_data is a numpy array
        if isinstance(self.elevation_data, np.ndarray):
            # Use scipy's zoom to resample the array
            self.elevation_data = zoom(self.elevation_data, zoom=scale_factor, order=3) # order=3 for bicubic interpolation
        else:
            raise TypeError("Elevation data must be a numpy array.")
    
    def fft_smooth(self, cutoff_frequency):
        """
        Applies FFT-based smoothing to the resampled elevation data.
        
        Parameters:
        - cutoff_frequency: Integer, the cutoff frequency for the FFT filter.
        """
        fft_data = np.fft.fft2(self.elevation_data)
        fft_shift = np.fft.fftshift(fft_data)
        
        rows, cols = self.elevation_data.shape
        crow, ccol = rows // 2, cols // 2
        
        mask = np.zeros((rows, cols), np.uint8)
        mask[crow-cutoff_frequency:crow+cutoff_frequency, ccol-cutoff_frequency:ccol+cutoff_frequency] = 1
        
        fft_shift_filtered = fft_shift * mask
        fft_inverse_shift = np.fft.ifftshift(fft_shift_filtered)
        self.smoothed_data = np.fft.ifft2(fft_inverse_shift)
        self.smoothed_data = np.abs(self.smoothed_data)
    
    def visualize_smoothed_data(self):
        """
        Visualizes the smoothed elevation data in 3D using a terrain colormap.
        """
        x_km = np.arange(self.smoothed_data.shape[1])
        y_km = np.arange(self.smoothed_data.shape[0])

        x=x_km*100
        y=y_km*100
        X, Y = np.meshgrid(x, y)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, self.smoothed_data, cmap='terrain', edgecolor='none')
        fig.colorbar(surf, shrink=0.5, aspect=5, label='Elevation (m)')
        
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Elevation (m)')
        #ax.view_init(elev=30, azim=120)

        scaling = [1, 1, 1]
        ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag(scaling + [1]))
        plt.show()




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

        x=x_km*100
        y=y_km*100
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


    
 
 