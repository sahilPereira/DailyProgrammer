'''
Created on Jan 18, 2016

@author: Sahil
'''
import operator
from _overlapped import NULL
import math

class LineSegment:
    x_1 = 0
    y_1 = 0
    x_2 = 0
    y_2 = 0
    point1 = NULL
    point2 = NULL
    
    def __init__(self, p1, p2):
        self.x_1 = p1.x
        self.y_1 = p1.y
        self.x_2 = p2.x
        self.y_2 = p2.y
        self.point1 = p1
        self.point2 = p2

class Point:
    x = 0
    y = 0
    min_angle = NULL
    max_angle = NULL
    visiblePoints = NULL
    
    def __init__(self, pointStr):
        point_values = pointStr.replace("(","").replace(")","").split(",")
        self.x = int(point_values[0])
        self.y = int(point_values[1])
        self.visiblePoints = {}
        
    def setX(self, newX):
        self.x = newX
        
    def setY(self, newY):
        self.y = newY
        
    def setMinAngle(self, min_angle):
        self.min_angle = min_angle
        
    def setMaxAngle(self, max_angle):
        self.max_angle = max_angle
        
    def setVisiblePoint(self, point, angle):
        self.visiblePoints[point] = angle
    
        
def getLineIntersection(l1, l2):
    
    delta_x_l1 = l1.x_2 - l1.x_1
    delat_y_l1 = l1.y_2 - l1.y_1
    delata_x_l2 = l2.x_2 - l2.x_1
    delata_y_l2 = l2.y_2 - l2.y_1
    
    denominator = (delta_x_l1*delata_y_l2 - delata_x_l2*delat_y_l1)
    if denominator != 0:
        s = (delta_x_l1 * (l1.y_1 - l2.y_1) - delat_y_l1 * (l1.x_1 - l2.x_1))/denominator
        t = (delata_x_l2 * (l1.y_1 - l2.y_1) - delata_y_l2 * (l1.x_1 - l2.x_1))/denominator
    
        if s>=0 and s<=1 and t>=0 and t<=1:
            # Collision detected
            return [l1.x_1 + (t*delta_x_l1), l1.y_1 + (t*delat_y_l1)]
    # if no collisions detected
    return -1

# based on the first and last line-segments
def isClockwise(line_segments):
    first_line = line_segments[0]
    last_line = line_segments[len(line_segments)-1]
    
    head_height = first_line.y_2
    tail_height = last_line.y_1
    
    if head_height > tail_height:
        # clockwise
        return True
    else:
        # counter-clockwise
        return False

# return the quadrant the head is pointed towards, 
# or the exact angle if the angle is a multiple of 90
def getQuadrant(tailPoint, headPoint):
        
    delta_x = headPoint.x - tailPoint.x
    delta_y = headPoint.y - tailPoint.y
    
    if (tailPoint.y == headPoint.y) and (headPoint.x > tailPoint.x):
        return 0
    elif (tailPoint.x == headPoint.x) and (headPoint.y > tailPoint.y):
        return 90
    elif (tailPoint.y == headPoint.y) and (headPoint.x < tailPoint.x):
        return 180
    if (tailPoint.x == headPoint.x) and (headPoint.y < tailPoint.y):
        return 270
    elif (delta_x > 0) and (delta_y > 0):
        return 1
    elif (delta_x < 0) and (delta_y > 0):
        return 2
    elif (delta_x < 0) and (delta_y < 0):
        return 3
    elif (delta_x > 0) and (delta_y < 0):
        return 4

# length of line between two points
def getMagnitude(point1, point2):
    
    delta_x = point1.x - point2.x
    delta_y = point1.y - point2.y
    return ((delta_x ** 2) + (delta_y ** 2)) ** (0.5)

# angle of line with respect to zero degrees
def getAngle(line):
    
    imaginary_point = Point('(0,1)')
    imaginary_point.setX(line.point1.x + 1)
    imaginary_point.setY(line.point1.y)
    
    magnitude_a = getMagnitude(imaginary_point, line.point2)
    magnitude_b = getMagnitude(line.point1, line.point2)    
    magnitude_c = 1;
    
    cos_a = ((magnitude_b ** 2) + (magnitude_c ** 2) - (magnitude_a ** 2)) / (2*magnitude_b*magnitude_c)
    angle_a = math.acos(cos_a) * 180 / math.pi
    return angle_a

# actual angle the line points towards
def getPointView(tailPoint, headPoint):
    
    tmp_line = LineSegment(tailPoint, headPoint)
    lineQuadrant = getQuadrant(tailPoint, headPoint)
    
    if lineQuadrant == 0 or lineQuadrant > 4:
        return lineQuadrant
    
    angleAtPoint = round(getAngle(tmp_line), 2)
    if lineQuadrant == 1 or lineQuadrant == 2:
        return angleAtPoint
    else:
        return 360 - angleAtPoint
    
def isInValidRange(point, angle, isGraphClockwise):
    
    # "min" angle is line_a, "max" angle is line_b
    real_min = min([point.min_angle, point.max_angle])
    real_max = max([point.min_angle, point.max_angle])
    if(real_max == angle or real_min == angle):
        return True
    
    isInRange = (real_min < angle) and (real_max > angle)
    if point.min_angle > point.max_angle:
        isInRange = not isInRange
    
    if isGraphClockwise:
        return isInRange
    else:
        return not isInRange

# addresses the condition that the camera can only view 180 degrees
def getMaxVisiblePoints(point, visible_points):
    
    # return all visible points if corner view is 180 degrees or less
    totalAngle = abs(point.min_angle - point.max_angle)
    if point.min_angle > point.max_angle:
        totalAngle = 360 - totalAngle
    totalAngle = totalAngle if isGraphClockwise else 360 - totalAngle
    if totalAngle <= 180:
        return point.visiblePoints
    
    # obtain the remaining hidden points from the list of visible points
    remaining_hidden_points = point.visiblePoints
    for key in visible_points:
        if key in remaining_hidden_points:
            del remaining_hidden_points[key]
            
#     sorted_angles = sorted(point.visiblePoints.items(), key=operator.itemgetter(1))
    sorted_angles = sorted(remaining_hidden_points.items(), key=operator.itemgetter(1))
    scaledList = []
    for x, item in enumerate(sorted_angles):
        what = (sorted_angles[x][0], item[1]+360)
        scaledList.append(what)
    # double the list of angles, so that we can do a virtual 360 sweep
    sorted_angles.extend(scaledList)
    
    start_index = 0
    end_index = 0
    maxAngles = 0
    start = sorted_angles[start_index][1]
    maxPos = len(sorted_angles)
    minPos = start_index
    while(end_index != len(sorted_angles)):
        end = sorted_angles[end_index][1]
        if abs(end-start) <= 180:
            end_index += 1
            continue
        else:
            if end_index-start_index > maxAngles:
                maxAngles = end_index-start_index
                minPos = start_index
                maxPos = end_index
            start_index += 1
            start = sorted_angles[start_index][1]
    # handle last case
    end = sorted_angles[end_index-1][1]
    if abs(end-start) <= 180:
        if end_index-start_index > maxAngles:
            maxAngles = end_index-start_index
            minPos = start_index
            maxPos = end_index
    totalAngle = sorted_angles[minPos:maxPos]
    newPointsSet = {}
    for x in totalAngle:
        newPointsSet[x[0]] = x[1]
    return newPointsSet
    

if __name__ == '__main__':
    
    with open('museumCamerasPoints.txt') as f:
        lines = f.readlines()
    input_list = lines[9].strip().split()
    
    # read all the points and make Point objects
    points = []
    for point in input_list:
        points.append(Point(point))
    
    # Build all the line segments from the point objects
    line_segments = []
    for idx, point in enumerate(points):
        if idx == len(points)-1:
            line_segments.append(LineSegment(points[idx], points[0]))
        else:
            line_segments.append(LineSegment(points[idx], points[idx+1]))
    
    isGraphClockwise = isClockwise(line_segments)
    
    # determine the view angles for each point
    for idx, point in enumerate(points):
        line1 = NULL
        line2 = line_segments[idx]
        if idx == 0:
            line1 = line_segments[len(line_segments)-1]
        else:
            line1 = line_segments[idx-1]
        
        point.setMinAngle(getPointView(line1.point2, line1.point1))
        point.setMaxAngle(getPointView(line2.point1, line2.point2))
    
    hidden_points = points
    for i, point in enumerate(points):
        # get angle between current point and other points
        for j, otherPoint in enumerate(points):
            if otherPoint != point:
                angle = getPointView(point, otherPoint)
                if (isInValidRange(point, angle, isGraphClockwise)):
                    # check intersects
                    vector = LineSegment(point, otherPoint)
                    intersectCounter = 0
                    for k, line in enumerate(line_segments):
                        line_intersect = getLineIntersection(vector, line)
                        if(line_intersect != -1): # -1 means there was no intersection
                            # check if the intersected line is the head/tail of the vector
                            if((line_intersect[0] != vector.x_1 and line_intersect[1] != vector.y_1)
                               and (line_intersect[0] != vector.x_2 and line_intersect[1] != vector.y_2)):
                                intersectCounter+=1
                    if intersectCounter < 1:
                        point.setVisiblePoint(otherPoint, angle)
    
    # corners where cameras will be placed
    final_corners = []
    point_with_best_view = NULL
    max_views = 0
    while True:
        for i, point in enumerate(hidden_points):
            if len(hidden_points) == 1:
                point_with_best_view = point
                break
            visible_points = list(set(points)^set(hidden_points))
            max_visible_points = getMaxVisiblePoints(point, visible_points)
            if len(max_visible_points) > max_views:
                max_views = len(max_visible_points)
                point_with_best_view = point
        if point_with_best_view in hidden_points:
            hidden_points.remove(point_with_best_view)
        for idx, y in enumerate(point_with_best_view.visiblePoints):
            if y in hidden_points:
                hidden_points.remove(y)
        final_corners.append(point_with_best_view)
        max_views = 0
        if len(hidden_points) == 0:
            break
    
    for i, finalPoint in enumerate(final_corners):
        print("(",finalPoint.x,",",finalPoint.y,")")
    
    
    
    
    
    
    
    
    
    