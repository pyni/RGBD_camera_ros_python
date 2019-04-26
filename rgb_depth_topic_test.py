#!/usr/bin/env python

""" 
Demo of reading from image topic, reading correspoding point cloud
information and using markers to show output in rviz.

Author: Peiyuan Ni
"""
import rospy

from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs import point_cloud2
import cv2
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker
import numpy as np
from message_filters import ApproximateTimeSynchronizer
import message_filters

 

class RedDepthNode(object):
    """ This node reads from the Kinect color stream and
    publishes an image topic with the most red pixel marked.
    Subscribes:
         /camera/rgb/image_color
    Publishes:
         red_marked_image
    """

    def __init__(self):
        """ Construct the red-pixel finder node."""
        rospy.init_node('red_depth_node')
        self.image_pub = rospy.Publisher('red_marked_image', Image,
                                         queue_size=10)
        self.marker_pub = rospy.Publisher('red_marker', Marker,
                                          queue_size=10)
        self.cv_bridge = CvBridge()

        # Unfortunately the depth data and image data from the kinect aren't
        # perfectly time-synchronized.  The code below handles this issue.
        img_sub = message_filters.Subscriber('/camera/rgb/image_raw', Image)
        dep_sub = message_filters.Subscriber(\
                            '/camera/depth/image_raw',
                            Image)
        self.kinect_synch = ApproximateTimeSynchronizer([img_sub, dep_sub],
                                                        queue_size=10,
                                                        slop=.02)

        self.kinect_synch.registerCallback(self.image_points_callback)

        rospy.spin()

    def image_points_callback(self, img, depth):
        """ Handle image/point_cloud callbacks. """
 
        # Convert the image message to a cv image object
        cv_img = self.cv_bridge.imgmsg_to_cv2(img, "bgr8")
        cv2.imwrite("./color_0.png", cv_img)

        cv_depth = self.cv_bridge.imgmsg_to_cv2(depth,"passthrough" ) 
        cv2.imwrite("./dep_1.png", cv_depth)
     #   print cv_depth.max()
        points_depth = np.uint8(cv_depth) 
#	
        cv2.imwrite("./dep_2.png", points_depth)


       # points_depth = np.float32([p/255.0 for p in points_depth]) 


      #  print np.array(points_depth).dtype.type,points_depth.max()



        points_depth = np.float32([p/1000.0 for p in cv_depth])    
        cv2.imwrite("./dep_3.png", points_depth)

        print np.array(points_depth).dtype.type,points_depth.max()

   
        np.save("./depth_0.npy",points_depth )
   
if __name__ == "__main__":
    r = RedDepthNode()

