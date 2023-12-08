import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_cube_mesh(cube_mesh):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for cube in cube_mesh:
        x = cube[0]  # X coordinates
        y = cube[1]  # Y coordinates
        z = cube[2]  # Z coordinates

        ax.plot(x, y, z, color='b')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cube Mesh Visualization')

    plt.show()

# Load cube mesh from JSON file
json_filename = "cube_mesh.json"
with open(json_filename, "r") as json_file:
    cube_mesh_list = json.load(json_file)

# Convert list to numpy array
cube_mesh = np.array(cube_mesh_list)

# Visualize the cube mesh
visualize_cube_mesh(cube_mesh)
