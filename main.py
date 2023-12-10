
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge
from nav_msgs.msg import OccupancyGrid, MapMetaData


MAP_SIZE = 100
MAP_RESOLUTION = 0.1
MAP_ORIGIN = (-MAP_SIZE / 2, -MAP_SIZE / 2)
LIDAR_MAX_RANGE = 10
LIDAR_MIN_ANGLE = -np.pi / 2
LIDAR_MAX_ANGLE = np.pi / 2
LIDAR_ANGLE_INCREMENT = np.pi / 180
DEPTH_MAX_RANGE = 5
DEPTH_FOV = np.pi / 4
DEPTH_ANGLE_INCREMENT = DEPTH_FOV / 320
OCCUPIED = 100
FREE = 0
UNKNOWN = -1

rospy.init_node('transbot_mapping')

bridge = CvBridge()


map = OccupancyGrid()
map.header.frame_id = 'map'
map.info.resolution = MAP_RESOLUTION
map.info.width = int(MAP_SIZE / MAP_RESOLUTION)
map.info.height = int(MAP_SIZE / MAP_RESOLUTION)
map.info.origin.position.x = MAP_ORIGIN[0]
map.info.origin.position.y = MAP_ORIGIN[1]
map.info.origin.orientation.w = 1
map.data = [UNKNOWN] * (map.info.width * map.info.height)


map_pub = rospy.Publisher('map', OccupancyGrid, queue_size=10)

def lidar_callback(scan):
    global map

    robot_x = scan.header.pose.position.x
    robot_y = scan.header.pose.position.y
    robot_theta = scan.header.pose.orientation.z

    robot_px = int((robot_x - MAP_ORIGIN[0]) / MAP_RESOLUTION)
    robot_py = int((robot_y - MAP_ORIGIN[1]) / MAP_RESOLUTION)

    for i in range(len(scan.ranges)):
        r = scan.ranges[i]
        theta = scan.angle_min + i * scan.angle_increment
        if r > scan.range_min and r < scan.range_max:
            x = robot_x + r * np.cos(robot_theta + theta)
            y = robot_y + r * np.sin(robot_theta + theta)
            px = int((x - MAP_ORIGIN[0]) / MAP_RESOLUTION)
            py = int((y - MAP_ORIGIN[1]) / MAP_RESOLUTION)
            if px >= 0 and px < map.info.width and py >= 0 and py < map.info.height:
                map.data[py * map.info.width + px] = OCCUPIED
                cv2.line(map.data, (robot_px, robot_py), (px, py), FREE)

def depth_callback(image):
    global map
    robot_x = image.header.pose.position.x
    robot_y = image.header.pose.position.y
    robot_theta = image.header.pose.orientation.z
    robot_px = int((robot_x - MAP_ORIGIN[0]) / MAP_RESOLUTION)
    robot_py = int((robot_y - MAP_ORIGIN[1]) / MAP_RESOLUTION)
    cv_image = bridge.imgmsg_to_cv2(image, '32FC1')
    for i in range(cv_image.shape[0]):
        for j in range(cv_image.shape[1]):
            d = cv_image[i, j]
            if d > 0 and d < DEPTH_MAX_RANGE:
                cx = (j - cv_image.shape[1] / 2) * d * np.tan(DEPTH_FOV / 2) / (cv_image.shape[1] / 2)
                cy = (i - cv_image.shape[0] / 2) * d * np.tan(DEPTH_FOV / 2) / (cv_image.shape[0] / 2)
                cz = d
                rx = cz
                ry = -cx
                rz = -cy
                x = robot_x + rx * np.cos(robot_theta) - ry * np.sin(robot_theta)
                y = robot_y + rx * np.sin(robot_theta) + ry * np.cos(robot_theta)
                px = int((x - MAP_ORIGIN[0]) / MAP_RESOLUTION)
                py = int((y - MAP_ORIGIN[1]) / MAP_RESOLUTION)
                if px >= 0 and px < map.info.width and py >= 0 and py < map.info.height:
                    map.data[py * map.info.width + px] = OCCUPIED
                    cv2.line(map.data, (robot_px, robot_py), (px, py), FREE)

lidar_sub = rospy.Subscriber('scan', LaserScan, lidar_callback)

depth_sub = rospy.Subscriber('image', Image, depth_callback)

def loop():
    global map
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        map.header.stamp = rospy.Time.now()
        map_pub.publish(map)
        rate.sleep()

loop()
