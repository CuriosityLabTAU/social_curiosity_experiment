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
publisher = rospy.Publisher('to_nao_left', String, queue_size=10)

threading._sleep(5)

print 'here-ui'
publisher.publish('{\"action\": \"move_to_pose\", \"parameters\": \"\\\"''center''\\\"\"}')
# time.sleep(2)

# publisher.publish('{\"action\": \"look_to_other_way\", \"parameters\": \"\\\"''center''\\\"\"}')
# publisher.publish('{\"action\": \"agree\"}')

threading._sleep(5)

import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import random
import time
import json

#
# animatedSpeech = ALProxy("ALAnimatedSpeech", '192.168.0.102', 9559)
# animatedSpeech.say('The Mona Lisa and Venus de Milo in the big-hitting Louvre are priceless Paris must-sees. Conveniently, quintessential Parisian gardens Jardin des Tuileries and Jardin du Palais Royal, with its elegant boutique-clad arcades, are next door', {"pitchShift": 1.0})
