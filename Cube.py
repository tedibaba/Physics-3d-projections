import numpy as np

class Cube:

    def __init__(self, theta_x, theta_y, theta_z, cube_origin, cube_side_len):
        self.cube_origin = np.matrix(cube_origin) #x,y,z
        self.theta_x = theta_x * (np.pi/180) 
        self.theta_y = theta_y * (np.pi/180) 
        self.theta_z = theta_z * (np.pi/180) 
        self.cube_side_len = cube_side_len
        self.cube_points = self.init_cube()

        self.faces = [[0,1,2,3], [0,1,5,4], [1,2,6,5], [0,4,7,3], [2,3,7,6], [4,5,6,7]]

    def init_cube(self):
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

    def project_2d(self, point):
        projection = np.matrix( [[1,0,0], [0,1,0]])
        res_point = np.dot(projection, point)

        return res_point
    
    def transform_points(self):
        res = []
        for i in range(len(self.cube_points)):
            rotated_point = self.rotate_cube(self.cube_points[i])
            # print(rotated_point, self.cube_origin)
            # print(np.add(self.cube_origin, rotated_point))
            res.append(self.project_2d(np.add(self.cube_origin, rotated_point)).flatten().tolist()[0])
            self.cube_points[i] = rotated_point
        return res
    
    def rotate_cube(self, point):
        rotation_x = np.matrix([[1,0,0], [0, np.cos(self.theta_x), -np.sin(self.theta_x)], [0, np.sin(self.theta_x), np.cos(self.theta_x)]])
        rotation_y = np.matrix([[np.cos(self.theta_y), 0, np.sin(self.theta_y)], [0,1,0], [-np.sin(self.theta_y), 0, np.cos(self.theta_y)]])
        rotation_z = np.matrix([[np.cos(self.theta_z), -np.sin(self.theta_z), 0], [np.sin(self.theta_z), np.cos(self.theta_z),0], [0,0,1]])

        complete_rotation = rotation_x @ rotation_y @ rotation_z

        res = complete_rotation @ point

        return res