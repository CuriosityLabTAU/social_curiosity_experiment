import rospy
from std_msgs.msg import String
# from nao_ros import NaoNode
import time
import random
import numpy as np
import time
import rospy
from std_msgs.msg import String
import sys
import json

import threading







def get_angles_nao():
    a= nao.get_angles()

    angels=''
    names=''
    for ang in a[0]:
        b=round(ang,2)
        angels=angels+','+str(b)

    for nam in a[1]:
        names=names+','+nam

    return names[1:]+';'+angels[1:]





rospy.init_node('ui')
publisher = rospy.Publisher('the_flow', String, queue_size=10)

threading._sleep(5)

print 'here-ui'
publisher.publish('60')

threading._sleep(5)