import rospy
from std_msgs.msg import String
# from naoqi import ALProxy
import sys
# import almath
import time
import datetime
import json

rospy.init_node('talker')

nao_movements = rospy.Publisher('nao_movements', String, queue_size=10)
nao_movements.publish('matan ')