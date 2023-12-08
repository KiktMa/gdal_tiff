import numpy as np
import json

def generate_cube_mesh(min_point, max_point, side_length):
    cube_side = side_length / 2.0

    x_values = np.arange(min_point[0], max_point[0], side_length)
    y_values = np.arange(min_point[1], max_point[1], side_length)
    z_values = np.arange(min_point[2], max_point[2], side_length)

    vertices = []
    for x in x_values:
        for y in y_values:
            for z in z_values:
                vertices.append([x - cube_side, y - cube_side, z - cube_side])
                vertices.append([x + cube_side, y - cube_side, z - cube_side])
                vertices.append([x + cube_side, y + cube_side, z - cube_side])
                vertices.append([x - cube_side, y + cube_side, z - cube_side])

    return np.array(vertices)

# Given minimum and maximum points
min_point = np.array([0.92738, 0.051462, 0.405092])
max_point = np.array([343.814, 309.04, 37.1431])

# Batch generate cube meshes with a side length of 2 meters
side_length = 2.0
cube_mesh = generate_cube_mesh(min_point, max_point, side_length)

# Convert numpy array to list for JSON serialization
cube_mesh_list = cube_mesh.tolist()

# Save to JSON file
json_filename = "cube_mesh.json"
with open(json_filename, "w") as json_file:
    json.dump(cube_mesh_list, json_file)

print(f"Cube mesh saved to {json_filename}")
