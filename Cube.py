import random
import numpy as np
from typing import List, Tuple

class Cube:
    """
    A Cube in 3d space
    """
    def __init__(self, theta_x : int , theta_y : int, theta_z : int, cube_origin :List[int], cube_side_len : int, view_point: Tuple[int]):
        """
        Initializes a Cube object.

        Parameters:
        - theta_x (int): The rotation angle around the x-axis in degrees.
        - theta_y (int): The rotation angle around the y-axis in degrees.
        - theta_z (int): The rotation angle around the z-axis in degrees.
        - cube_origin (List[int]): The origin point of the cube in 3D space.
        - cube_side_len (int): The length of each side of the cube.
        - view_point (Tuple[int]): The viewpoint from which the cube is observed.
        """
        self.cube_origin = np.matrix(cube_origin) #x,y,z
        self.theta_x = theta_x * (np.pi/180) 
        self.theta_y = theta_y * (np.pi/180) 
        self.theta_z = theta_z * (np.pi/180) 
        self.cube_side_len = cube_side_len
        self.cube_points = self.init_cube()
        self.manual_rotatable = False
        self.view_point = view_point
        self.faces = [[0,1,2,3], [4,5,1,0], [6,2,1,5], [3,7,4,0], [3,2,6,7], [6,5,4,7], ] #Organised as cross product friendly

    def init_cube(self):
        """
        Initializes the 3D coordinates of the cube's vertices.

        Returns:
        - List[np.matrix]: The 3D coordinates of the cube's vertices.
        """
        #First 4 are the top of the cube, last 4 are bottom 4 points
        points = [np.transpose(np.matrix([- self.cube_side_len / 2,  + self.cube_side_len/2,  + self.cube_side_len / 2])),
                  np.transpose(np.matrix([+ self.cube_side_len / 2,  + self.cube_side_len/2,  + self.cube_side_len / 2])),
                  np.transpose(np.matrix([+ self.cube_side_len / 2,  - self.cube_side_len/2,  + self.cube_side_len / 2])),
                  np.transpose(np.matrix([- self.cube_side_len / 2,  - self.cube_side_len/2,  + self.cube_side_len / 2])),
                  np.transpose(np.matrix([- self.cube_side_len / 2,  + self.cube_side_len/2,  - self.cube_side_len / 2])),
                  np.transpose(np.matrix([+ self.cube_side_len / 2,  + self.cube_side_len/2,  - self.cube_side_len / 2])),
                  np.transpose(np.matrix([+ self.cube_side_len / 2,  - self.cube_side_len/2,  - self.cube_side_len / 2])),
                  np.transpose(np.matrix([- self.cube_side_len / 2,  - self.cube_side_len/2,  - self.cube_side_len / 2]))]

        return points

    def project_2d(self, point: np.matrix):
        """
        Projects a 3D point onto a 2D plane.

        Args:
            point (np.matrix): The 3D point to be projected.

        Returns:
            np.matrix: The projected 2D point.
        """
        projection = np.matrix([[1, 0, 0], [0, 1, 0]])
        res_point = np.dot(projection, point)

        return res_point
    
    def transform_points(self):
        """
        Transforms the points of the cube by rotating them and projecting them onto a 2D plane.

        Returns:
            list: A list of transformed points in 2D space.
        """
        res = []

        for i in range(len(self.cube_points)):
            rotated_point = self.rotate_cube(self.cube_points[i])
            res.append(self.project_2d(np.add(self.cube_origin, rotated_point)).flatten().tolist()[0])
            self.cube_points[i] = rotated_point
        
        return res
    
    def visible_faces(self):
        """
        Returns a list of visible faces of the cube.

        This method iterates through each face of the cube and checks if it is visible.
        A face is considered visible if its normal vector is facing towards the viewer.
        The visible faces are stored in a list along with their corresponding indices.

        Returns:
            list: A list of tuples containing the index and face of each visible face.

        """
        visible_faces = []
        
        for i, face in enumerate(self.faces):
            face_cross_vec = self.find_face_perp(face)
            if self.visible(face_cross_vec):
                visible_faces.append((i, face))
        
        return self.painter_algorithm(visible_faces)
    
    def rotate_cube(self, point: np.matrix):
        """
        Rotates the given point in 3D space using the specified rotation angles.

        Args:
            point (np.matrix): The point to be rotated, represented as a 3x1 matrix.

        Returns:
            np.matrix: The rotated point, represented as a 3x1 matrix.
        """
        rotation_x = np.matrix([[1, 0, 0], [0, np.cos(self.theta_x), -np.sin(self.theta_x)], [0, np.sin(self.theta_x), np.cos(self.theta_x)]])
        rotation_y = np.matrix([[np.cos(self.theta_y), 0, np.sin(self.theta_y)], [0, 1, 0], [-np.sin(self.theta_y), 0, np.cos(self.theta_y)]])
        rotation_z = np.matrix([[np.cos(self.theta_z), -np.sin(self.theta_z), 0], [np.sin(self.theta_z), np.cos(self.theta_z), 0], [0, 0, 1]])

        complete_rotation = rotation_x @ rotation_y @ rotation_z

        res = complete_rotation @ point

        return res
    
    def change_rotation_values(self, spread: int):
        """
        Changes the rotation values of the cube by setting theta_x, theta_y, and theta_z to random values within the given spread.

        Parameters:
        spread (int): The range within which the rotation values can vary.

        Returns:
        None
        """
        val = random.uniform(-spread, spread)
        self.theta_x = val
        self.theta_y = val
        self.theta_z = val

    def find_face_perp(self, face: List[int]):
        """
        Calculates the perpendicular vector to a face of the cube.

        Args:
            face (List[int]): List of indices representing the vertices of the face.

        Returns:
            numpy.ndarray: The perpendicular vector to the face.
        """
        point1 = self.cube_points[face[0]]
        point2 = self.cube_points[face[1]]
        point3 = self.cube_points[face[2]]

        vec1 = np.transpose(np.subtract(point1, point2))
        vec2 = np.transpose(np.subtract(point3, point2))
        return np.cross(vec1, vec2)

    def visible(self, face_cross_vec: np.matrix):
        """
        Determines if a face is visible based on the cross product of the face normal vector and the view point vector.

        Parameters:
        face_cross_vec (np.matrix): The cross product of the face normal vector and the view point vector.

        Returns:
        bool: True if the face is visible, False otherwise.
        """
        return (face_cross_vec @ self.view_point) > 0


    def painter_algorithm(self, visible_faces: List[Tuple[int, List[int]]]):
        """
        Sorts the visible faces based on the distance from the z-values.

        Args:
            visible_faces (List[Tuple[int, List[int]]]): A list of visible faces, where each face is represented as a tuple
            containing the face index and a list of vertex indices.

        Returns:
            List[Tuple[int, List[int]]]: The sorted list of visible faces.
        """
        return sorted(visible_faces, key=lambda face: min([self.cube_points[i][2] for i in face[1]]))
