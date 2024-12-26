import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

class DraggablePoints:
    def __init__(self):
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        
        # Generate circle
        self.center = np.array([0.5, 0.5])
        self.radius = 0.3
        self.num_points = 100
        t = np.linspace(0, 2*np.pi, self.num_points)
        self.x = self.center[0] + self.radius * np.cos(t)
        self.y = self.center[1] + self.radius * np.sin(t)
        
        self.loop_line, = self.ax.plot(self.x, self.y, 'w-', zorder=1)
        self.ax.text(self.x[0], self.y[0], '0.0/1.0', color='white', ha='right')
        
        # Generate random points
        angles = np.random.rand(4) * 2 * np.pi
        points = [self.center + self.radius * np.array([np.cos(angle), np.sin(angle)]) 
                 for angle in angles]
        
        # Create draggable points
        self.points = [
            Circle(points[0], 0.02, fc='yellow', zorder=3),
            Circle(points[1], 0.02, fc='magenta', zorder=3),
            Circle(points[2], 0.02, fc='sandybrown', zorder=3),
            Circle(points[3], 0.02, fc='palevioletred', zorder=3)
        ]
        
        # Create connection lines
        self.connection_lines = [
            Line2D([points[0][0], points[1][0]], 
                  [points[0][1], points[1][1]], 
                  c='cyan', zorder=2),
            Line2D([points[2][0], points[3][0]], 
                  [points[2][1], points[3][1]], 
                  c='cyan', zorder=2)
        ]
        
        # Create midpoints
        self.midpoints = [
            Circle(self.get_midpoint(points[0], points[1]), 0.015, fc='teal', zorder=3),
            Circle(self.get_midpoint(points[2], points[3]), 0.015, fc='teal', zorder=3)
        ]
        
        # Create intersection point and rectangle (initially hidden)
        self.intersection_point = Circle((0, 0), 0.01, fc='springgreen', zorder=4, visible=False)
        self.rectangle_lines = [
            Line2D([], [], c='gold', linestyle='--', alpha=0.6, zorder=1),
            Line2D([], [], c='gold', linestyle='--', alpha=0.6, zorder=1),
            Line2D([], [], c='gold', linestyle='--', alpha=0.6, zorder=1),
            Line2D([], [], c='gold', linestyle='--', alpha=0.6, zorder=1)
        ]
        
        # Add elements to plot
        for point in self.points + self.midpoints:
            self.ax.add_patch(point)
        for line in self.connection_lines + self.rectangle_lines:
            self.ax.add_line(line)
        self.ax.add_patch(self.intersection_point)
        
        # Setup interaction
        self.selected_point = None
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        # Set dark background and grid
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        
        # Major grid - center lines white, others turquoise
        self.ax.grid(True, color='darkturquoise', alpha=0.15, linewidth=1)
        self.ax.axhline(y=0.5, color='white', alpha=0.3, linewidth=1)
        self.ax.axvline(x=0.5, color='white', alpha=0.3, linewidth=1)
        
        # Minor grid
        self.ax.grid(True, which='minor', color='darkturquoise', alpha=0.05, linewidth=0.5)
        self.ax.set_xticks(np.arange(0, 1.1, 0.1))
        self.ax.set_yticks(np.arange(0, 1.1, 0.1))
        self.ax.set_xticks(np.arange(0, 1.01, 0.02), minor=True)
        self.ax.set_yticks(np.arange(0, 1.01, 0.02), minor=True)
        
        self._update_coordinates()

    def get_midpoint(self, p1, p2):
        """Calculate midpoint between two points"""
        if isinstance(p1, Circle):
            p1 = p1.center
        if isinstance(p2, Circle):
            p2 = p2.center
        return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)

    def get_loop_coordinate(self, point):
        """Convert point position to loop coordinate (0.0 to 1.0)"""
        angle = np.arctan2(point[1] - self.center[1], point[0] - self.center[0])
        if angle < 0:
            angle += 2 * np.pi
        return angle / (2 * np.pi)

    def project_point_to_circle(self, point):
        """Project a point onto the circle"""
        vector = point - self.center
        normalized = vector / np.linalg.norm(vector)
        return self.center + normalized * self.radius

    def on_press(self, event):
        if event.inaxes != self.ax: return
        for point in self.points:
            if np.sqrt((event.xdata - point.center[0])**2 + 
                      (event.ydata - point.center[1])**2) < point.radius:
                self.selected_point = point
                break

    def on_motion(self, event):
        if self.selected_point is None or event.inaxes != self.ax: return
        
        new_point = self.project_point_to_circle(np.array([event.xdata, event.ydata]))
        self.selected_point.center = tuple(new_point)
        
        self._update_connection()
        self._update_coordinates()
        self._update_intersection()
        self._update_midpoints()
        self.fig.canvas.draw_idle()

    def on_release(self, event):
        self.selected_point = None

    def _update_connection(self):
        self.connection_lines[0].set_data([self.points[0].center[0], self.points[1].center[0]],
                                        [self.points[0].center[1], self.points[1].center[1]])
        self.connection_lines[1].set_data([self.points[2].center[0], self.points[3].center[0]],
                                        [self.points[2].center[1], self.points[3].center[1]])

    def _update_intersection(self):
        m1 = self.midpoints[0].center
        m2 = self.midpoints[1].center
        
        # Check if midpoints are close enough to be considered intersecting
        dist = np.sqrt((m1[0] - m2[0])**2 + (m1[1] - m2[1])**2)
        if dist < 0.02:  # Threshold for intersection
            # Draw connecting lines between points with wrap-around
            points = [self.points[0], self.points[2], self.points[3], self.points[1]]
            for i in range(4):
                self.rectangle_lines[i].set_data(
                    [points[i].center[0], points[(i+1)%4].center[0]],
                    [points[i].center[1], points[(i+1)%4].center[1]]
                )
            for line in self.rectangle_lines:
                line.set_visible(True)
                line.set_linestyle('--')
        else:
            for line in self.rectangle_lines:
                line.set_visible(False)

    def _update_midpoints(self):
        self.midpoints[0].center = self.get_midpoint(self.points[0], self.points[1])
        self.midpoints[1].center = self.get_midpoint(self.points[2], self.points[3])

    def _update_coordinates(self):
        for artist in self.ax.texts[1:]:
            artist.remove()
        for point in self.points:
            coord = self.get_loop_coordinate(point.center)
            self.ax.text(point.center[0], point.center[1] - 0.05,
                       f'{coord:.2f}', color=point.get_facecolor(),
                       horizontalalignment='center')

# Create and show visualization
viz = DraggablePoints()
plt.show()