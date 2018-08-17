import numpy as np
import time
import rospy
from std_msgs.msg import String
import operator
import sys
import json
import random
import pandas as pd
from numpy.random import choice

class dynamics():
    def __init__(self):
        rospy.init_node('test2')

        self.publisher_alive = rospy.Publisher('test', String, queue_size=10)




        rospy.Subscriber('tablet_game', String, self.update_current_answer)

        rospy.spin()


    def update_current_answer(self,data):
        if data.data=='1':
            self.publisher_alive.publish('123')



a=dynamics()

a=dynamics()