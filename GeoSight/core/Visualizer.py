import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import math
import contextily as ctx
import geopandas as gpd
from shapely.geometry import box

class ElevationDataVisualizer:
    """
    A class to visualize elevation data and compute dip and strike from clicked points.
    Also saves a satellite image based on corner coordinates.
    """

    def __init__(self, elevation_data):
        self.elevation_data = elevation_data
        self.clicked_points = []
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

    def visualize_elevation_data(self):
        """
        Visualizes the elevation data and enables point selection.
        """
        mappable = self.ax.imshow(self.elevation_data, cmap='terrain')
        plt.colorbar(mappable, label='Elevation (m)')
        plt.savefig('GeoSight/output/Elevation_plot.png')

        # Connect the click event
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()

    def onclick(self, event):
        """
        Handles click events on the map to record 3D points.
        """
        ix, iy = event.xdata, event.ydata
        if ix is not None and iy is not None and len(self.clicked_points) < 3:
            idx = int(np.round(ix))
            idy = int(np.round(iy))

            if 0 <= idy < self.elevation_data.shape[0] and 0 <= idx < self.elevation_data.shape[1]:
                iz = self.elevation_data[idy, idx]
                label = f"P{len(self.clicked_points)+1}"
                self.clicked_points.append((label, ix, iy, iz))
                self.ax.plot(ix, iy, 'o', markersize=7, color='yellow')
                self.ax.annotate(label, (ix, iy), textcoords="offset points", xytext=(0, 10), ha='center')
                self.fig.canvas.draw()

                if len(self.clicked_points) == 3:
                    self.show_data()

    def calculate_dip_and_strike(self):
        """
        Calculates dip and strike from the three clicked points.
        """
        _, x1, y1, z1 = self.clicked_points[0]
        _, x2, y2, z2 = self.clicked_points[1]
        _, x3, y3, z3 = self.clicked_points[2]

        P1 = np.array([x1, y1, z1])
        P2 = np.array([x2, y2, z2])
        P3 = np.array([x3, y3, z3])

        v1 = P2 - P1
        v2 = P3 - P1
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)

        dip = np.degrees(np.arccos(abs(normal[2]) / norm))
        strike = (np.degrees(np.arctan2(normal[1], normal[0])) + 90) % 360

        return dip, strike

    def show_data(self):
        """
        Opens a Tkinter window to display the clicked points and dip/strike.
        """
        window = tk.Tk()
        window.title("Elevation Data")
        headers = ["Point", "X", "Y", "Elevation"]
        for i, header in enumerate(headers):
            tk.Label(window, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=i)

        for index, (label, x, y, z) in enumerate(self.clicked_points):
            tk.Label(window, text=label).grid(row=index+1, column=0)
            tk.Label(window, text=f"{x:.2f}").grid(row=index+1, column=1)
            tk.Label(window, text=f"{y:.2f}").grid(row=index+1, column=2)
            tk.Label(window, text=f"{z:.2f}").grid(row=index+1, column=3)

        if len(self.clicked_points) == 3:
            dip, strike = self.calculate_dip_and_strike()
            next_row = len(self.clicked_points) + 2
            tk.Label(window, text="Dip (°):", font=('Helvetica', 10, 'bold')).grid(row=next_row, column=0, sticky='e')
            tk.Label(window, text=f"{dip:.2f}").grid(row=next_row, column=1, sticky='w')
            tk.Label(window, text="Strike (°):", font=('Helvetica', 10, 'bold')).grid(row=next_row + 1, column=0, sticky='e')
            tk.Label(window, text=f"{strike:.2f}").grid(row=next_row + 1, column=1, sticky='w')

        window.mainloop()

    def save_satellite_image(self, corner_coords, filename="GeoSight/output/satellite_map.png"):
        """
        Saves a satellite image using the provided corner coordinates.
        """
        if not corner_coords:
            print("No coordinates provided.")
            return

        tl, tr, br, bl = corner_coords  # top-left, top-right, bottom-right, bottom-left
        minx = min(tl[0], bl[0])
        miny = min(bl[1], br[1])
        maxx = max(tr[0], br[0])
        maxy = max(tl[1], tr[1])

        poly = box(minx, miny, maxx, maxy)
        gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[poly])
        gdf = gdf.to_crs(epsg=3857)

        fig, ax = plt.subplots(figsize=(8, 8))
        gdf.boundary.plot(ax=ax, edgecolor="red", linewidth=2)
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery)
        ax.set_axis_off()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Satellite image saved to: {filename}")

