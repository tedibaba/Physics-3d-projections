import numpy as np
from collections import deque, defaultdict
 
#Retracing through distance to viewer

def quick_trace(external_points, view_point):
    points = flood_fill(external_points)
    distances = [trace_distance_to_viewer(point, view_point) for point in points]
    # for point in points:
    #     distrace_distance_to_viewer(point, view_point)
    return zip(scales_values(distances), points)

def trace_distance_to_viewer(point, view_point):
    #Sort the faces based on the distance from the coords-values
    #Retracing through distance to viewer
    return np.linalg.norm(np.subtract(point, view_point))

def scales_values(points, min_val, max_val):

    # points.sort(key=lambda x: x[2])
    # min_val = points[0][2]
    # max_val = points[-1][2]
    scaled_points = [255 * ((point - min_val) / (max_val - min_val)) for point in points]
    return scaled_points

def assign_color(scale):
    return (255 - scale, 255 - scale, 255 - scale)

#Save in memory to speed up computation in future iterations with same points
def flood_fill(external_points):
    start = external_points[0]
    visited = defaultdict(lambda: False)
    q = deque()
    q.append(start)
    dh = (-1, 0, 0, 1, -1, 0, 0, 1, -1, 0, 0, 1)
    dv = (0,-1, 1, 0,0,-1, 1, 0, 0,-1, 1, 0 )
    dz = (0,0,0,0,1,1,1,1,-1,-1,-1,-1)
    polygon = [start]
    while q:
        pnt = q.popleft()
        for i in range(len(dh)):
            #Check within the polygon
            check_pnt = (pnt[0] + dh[i], pnt[1] + dv[i], pnt[2] + dz[i])
            if not visited[check_pnt] and pnpoly(external_points, check_pnt):
                polygon.append(check_pnt)
                q.append(check_pnt)
                visited[check_pnt] = True
                print(check_pnt)
    return polygon

def pnpoly(points, test_point):
    c = 0
    j = len(points) - 1
    for i in range(len(points)):
        if ((points[i][1] > test_point[1]) != (points[j][1] > test_point[1])) and \
                (test_point[0] < (points[j][0] - points[i][0]) * (test_point[1] - points[i][1]) / (points[j][1] - points[i][1]) + points[i][0]):
            c = not c
        j = i
    return c