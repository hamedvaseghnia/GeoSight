import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import zoom
import pyvista as pv
from sklearn.model_selection import ParameterGrid
from sklearn.base import BaseEstimator, TransformerMixin

class ElevationDataProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, elevation_data, scale_factor=1.0, cutoff_frequency=10):
        self.elevation_data = elevation_data
        self.scale_factor = scale_factor
        self.cutoff_frequency = cutoff_frequency
        self.smoothed_data = None

    def fit(self, X=None, y=None):
        return self

    def transform(self, X=None):
        original_data = self.elevation_data.copy()
        self.resample_elevation_data(self.scale_factor)
        self.fft_smooth(self.cutoff_frequency)
        residuals = self.compute_residuals(original_data)
        return residuals

    def resample_elevation_data(self, scale_factor):
        if isinstance(self.elevation_data, np.ndarray):
            self.elevation_data = zoom(self.elevation_data, zoom=scale_factor, order=3)
        else:
            raise TypeError("Elevation data must be a numpy array.")

    def fft_smooth(self, cutoff_frequency):
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

    def upsample_smoothed_data(self, original_shape):
        if self.smoothed_data is None:
            raise ValueError("Smoothed data is not available. Please run fft_smooth first.")
        scale_factors = [o / s for o, s in zip(original_shape, self.smoothed_data.shape)]
        return zoom(self.smoothed_data, zoom=scale_factors, order=3)
    
    def compute_residuals(self, original_data=None):
        if original_data is None:
            original_data = self.elevation_data
        original_shape = original_data.shape
        upsampled_data = self.upsample_smoothed_data(original_shape)
        residuals = original_data - upsampled_data
        return residuals

    def plot_residuals(self):
        residuals = self.compute_residuals()
        plt.figure(figsize=(10, 8))
        contour = plt.contourf(residuals, cmap='RdBu')
        plt.colorbar(contour, label='Residuals (m)')
        plt.title('Residual Contour Plot')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

    def visualize_smoothed_data(self):
        x_km = np.arange(self.smoothed_data.shape[1])
        y_km = np.arange(self.smoothed_data.shape[0])

        x = x_km * 100
        y = y_km * 100
        X, Y = np.meshgrid(x, y)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, self.smoothed_data, cmap='terrain', edgecolor='none')
        fig.colorbar(surf, shrink=0.5, aspect=5, label='Elevation (m)')
        
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Elevation (m)')

        scaling = [1, 1, 1]
        ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag(scaling + [1]))
        plt.show()

    def export_to_vtk(self, filename):
        if self.smoothed_data is None:
            raise ValueError("Smoothed data is not available. Please run fft_smooth first.")
        
        nx, ny = self.smoothed_data.shape
        nz = 1
        
        x_km = np.linspace(0, nx-1, nx)
        y_km = np.linspace(0, ny-1, ny)

        x = x_km * 100
        y = y_km * 100
        z = np.zeros((nx, ny))
        X, Y = np.meshgrid(x, y, indexing='ij')
        
        Z = self.smoothed_data
        points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
        
        grid = pv.StructuredGrid()
        grid.points = points
        grid.dimensions = [nx, ny, nz]
        
        grid.point_data["elevation"] = Z.flatten(order='C')
        
        grid.save(filename, binary=False)
        print(f"Exported 3D structured grid to {filename} in ASCII format.")

    def find_best_parameters(self):
        param_grid = {
            'scale_factor': [0.5, 0.75, 1, 1.25, 1.5],
            'cutoff_frequency': [5, 10, 20, 30, 40]
        }
        best_params = None
        best_score = float('inf')
        for params in ParameterGrid(param_grid):
            self.scale_factor = params['scale_factor']
            self.cutoff_frequency = params['cutoff_frequency']
            residuals = self.transform()
            score = np.mean(residuals**2)
            if score < best_score:
                best_score = score
                best_params = params

        print(f"Best parameters: {best_params}")
        print(f"Best score: {best_score}")


