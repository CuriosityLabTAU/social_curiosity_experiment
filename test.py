import rospy
from std_msgs.msg import String
# from naoqi import ALProxy
import sys
# import almath
import time
import datetime
import json

rospy.init_node('matan')

nao_movements = rospy.Publisher('to_nao', String, queue_size=10)
nao_movements.publish('matan')