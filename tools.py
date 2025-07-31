from plotly import graph_objects as go
import numpy as np

sbnd_det_box = {
    'x': np.array([-200,200]),
    'y': np.array([-200,200]),
    'z': np.array([0, 500])
}

pdg_color_name_dict = {
    11: ['blue',  'e-'],
    12: ['blue',  'nu_e'],
    13: ['red',   'mu-'],
    14: ['red',   'nu_mu'],
    211: ['green', 'pi+'],
    111: ['darkgreen', 'pi0'],
    321: ['orange', 'K+'],
    311: ['yellow', 'K0L'],
    221: ['purple', 'eta'],
    22: ['black', 'gamma'],
}

def make_detector_box(fig, xlims=sbnd_det_box['x'], ylims=sbnd_det_box['y'], zlims=sbnd_det_box['z']):
    
    fig.add_trace(
        go.Scatter3d(
            x=[xlims[0], xlims[1], xlims[1], xlims[0], xlims[0],xlims[0], xlims[1], xlims[1], xlims[0], xlims[0], xlims[0], xlims[0], xlims[1], xlims[1], xlims[1], xlims[1], 0, 0, 0, 0, 0],
            y=[zlims[0], zlims[0], zlims[1], zlims[1], zlims[0], zlims[0], zlims[0], zlims[1], zlims[1], zlims[0], zlims[1], zlims[1], zlims[1], zlims[1],zlims[0], zlims[0], zlims[0], zlims[0], zlims[1], zlims[1], zlims[0]],
            z=[ylims[0], ylims[0], ylims[0], ylims[0], ylims[0], ylims[1], ylims[1], ylims[1], ylims[1], ylims[1], ylims[1], ylims[0], ylims[0], ylims[1], ylims[1], ylims[0],ylims[0], ylims[1], ylims[1], ylims[0], ylims[0]],
            mode='lines',
            line=dict(color='lightgrey', width=2),
            name='Detector Box'
        )
    )
    return fig

def rodrigues_rotation(vector, axis, angle):
    # Angle must be in radians
    vector = np.array(vector)
    axis = np.array(axis)
    axis = axis / np.linalg.norm(axis)  # Normalize the axis vector

    return vector * np.cos(angle) + np.cross(axis, vector) * np.sin(angle) + axis * np.dot(axis, vector) * (1 - np.cos(angle))

def plot_shower_cone(fig, start_coordinates, end_coordinates, opening_angle, shower_name=None, color='blue', addLegend=True):
    shower_axis = np.array(end_coordinates) - np.array(start_coordinates)
    length = np.linalg.norm(shower_axis)
    base_radius = np.tan(np.radians(opening_angle / 2)) * length  # Radius of the cone base

    perp_vector = np.cross(shower_axis, [0, 0, 1])  # Get a vector perpendicular to the axis
    angles = np.linspace(0, 2 * np.pi, 20, endpoint=False)  # Don't include endpoint to avoid duplicate

    base_points = []

    # Generate base circle points (DO NOT add start_coordinates here)
    for angle in angles:
        rotated_vector = rodrigues_rotation(perp_vector, shower_axis, angle)
        rotated_vector = rotated_vector / np.linalg.norm(rotated_vector)  # Normalize the vector

        base_point = [end_coordinates[0] + rotated_vector[0] * base_radius,
                      end_coordinates[1] + rotated_vector[1] * base_radius,
                      end_coordinates[2] + rotated_vector[2] * base_radius]
        base_points.append(base_point)

    n_points = len(base_points)

    # Vertex list: apex first, then base circle points, then base center
    vertices = [start_coordinates] + base_points + [end_coordinates]

    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    z_coords = [v[2] for v in vertices]

    # Define triangular faces using indices
    i_coords, j_coords, k_coords = [], [], []

    # Cone side faces: connect apex (0) to base circle
    for i in range(n_points):
        next_i = (i + 1) % n_points
        # Triangle: apex -> base[i] -> base[next_i]
        i_coords.append(0)  # apex
        j_coords.append(i + 1)  # current base point (offset by 1)
        k_coords.append(next_i + 1)  # next base point

    # Base faces: connect base center to base circle
    base_center_idx = n_points + 1  # index of base center
    for i in range(n_points):
        next_i = (i + 1) % n_points
        # Triangle: apex -> base[i] -> base[next_i]
        i_coords.append(0)  # apex
        j_coords.append(i + 1)  # current base point (offset by 1)
        k_coords.append(next_i + 1)  # next base point

    # Base faces: connect base center to base circle
    base_center_idx = n_points + 1  # index of base center
    for i in range(n_points):
        next_i = (i + 1) % n_points
        # Triangle: base_center -> base[next_i] -> base[i] (note the order for correct normal)
        i_coords.append(base_center_idx)  # base center
        j_coords.append(next_i + 1)  # next base point
        k_coords.append(i + 1)  # current base point


    fig.add_trace(
        go.Mesh3d(
            x=x_coords, 
            y=z_coords, 
            z=y_coords,
            i=i_coords,  # First vertex of each triangle
            j=k_coords,  # Second vertex of each triangle  
            k=j_coords,  # Third vertex of each triangle
            opacity=0.25,
            color=color,
            name=shower_name,
            showlegend=addLegend,
        )
    )

    return fig