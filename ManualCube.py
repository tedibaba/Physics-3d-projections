from Cube import Cube

class ManualCube(Cube):
    
    def __init__(self, theta_x, theta_y, theta_z, cube_origin, cube_side_len, view_point):
        super().__init__(theta_x, theta_y, theta_z, cube_origin, cube_side_len, view_point)
        self.manual_rotatable = True
    def manual_rotate_x(self, value):
        self.theta_x = value
    def manual_rotate_y(self, value):
        self.theta_y = value
    def manual_rotate_z(self, value):
        self.theta_z = value
        
