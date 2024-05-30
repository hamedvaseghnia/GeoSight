import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import math

class ElevationDataVisualizer:
    """
    A class to visualize elevation data.
    """

    def __init__(self, elevation_data):
        """
        Initializes the visualizer with loaded elevation data.
        
        Parameters:
        - elevation_data: Array-like, the elevation data to visualize.
        """
        self.elevation_data = elevation_data
        self.clicked_points = []
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

    def visualize_elevation_data(self):
        """
        Visualizes the loaded elevation data using a terrain color map.
        """
        mappable = self.ax.imshow(self.elevation_data, cmap='terrain')
        plt.colorbar(mappable, label='Elevation (m)')
        plt.savefig('GeoSight/output/Elevation_plot.png')

        # Connect the event handler for mouse clicks
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()

    def onclick(self, event):
        """
        Event handler for mouse clicks to capture and annotate points on the plot.
        """
        ix, iy = event.xdata, event.ydata
        if ix is not None and iy is not None and len(self.clicked_points) < 3:
            idx = int(np.round(ix))
            idy = int(np.round(iy))
            iz = self.elevation_data[idy, idx]
            label = f"P{len(self.clicked_points)+1}"

            self.clicked_points.append((label, ix, iy, iz))
            self.ax.plot(ix, iy, 'o', markersize=7, label=label)
            self.ax.annotate(label, (ix, iy), textcoords="offset points", xytext=(0, 10), ha='center')
            self.fig.canvas.draw()

            if len(self.clicked_points) == 3:
                _, p2_x, p2_y, _ = self.clicked_points[1]
                self.draw_v_shape(p2_x, p2_y)
                self.show_data()

    def draw_v_shape(self, x, y):
        """
        Draws V-shaped lines near a specified point.
        """
        line_length = 0.5
        angle = 45
        radians = math.radians(angle)
        self.ax.plot([x, x + line_length * math.cos(radians)], [y, y + line_length * math.sin(radians)], 'k-', lw=2, color='red')
        self.ax.plot([x, x + line_length * math.cos(radians + math.pi / 2)], [y, y + line_length * math.sin(radians + math.pi / 2)], 'k-', lw=2, color='red')
        self.fig.canvas.draw()

    def show_data(self):
        """
        Displays the captured points data in a new Tkinter window.
        """
        window = tk.Tk()
        window.title("Elevation Data")
        headers = ["Point", "Longitude", "Latitude", "Elevation"]
        for i, header in enumerate(headers):
            tk.Label(window, text=header, font=('Helvetica', 0, 'bold')).grid(row=0, column=i)
        
        for index, (label, x, y, z) in enumerate(self.clicked_points):
            tk.Label(window, text=label).grid(row=index+1, column=0)
            tk.Label(window, text=f"{x:.2f}").grid(row=index+1, column=1)
            tk.Label(window, text=f"{y:.2f}").grid(row=index+1, column=2)
            tk.Label(window, text=f"{z:.2f}").grid(row=index+1, column=3)
        
        window.mainloop()
