import rospy
from std_msgs.msg import String
# from naoqi import ALProxy
import sys
# import almath
import time
import datetime
import json


class NaoNode():

    def __init__(self, robot_ip=list):
        self.number_of_robots=len(robot_ip)
        self.port = 9559
        self.robot_ip={}

        for i in range(self.number_of_robots):
            robot_ip[i]= robot_ip[i]


        # try:
        #     self.motionProxy={}                 #motionProxy
        #     self.postureProxy ={}               #postureProxy
        #     self.animatedSpeech={}              #animatedSpeech
        #
        #     for i in range(self.number_of_robots):
        #
        #         #motionProxy
        #         self.motionProxy[i] = ALProxy("ALMotion", self.robot_ip[i], self.port)
        #
        #         # postureProxy
        #         self.postureProxy[i] = ALProxy("ALRobotPosture", self.robot_ip[i], self.port)
        #
        #         # animatedSpeech
        #         self.animatedSpeech[i] = ALProxy("ALAnimatedSpeech", self.robot_ip[i], self.port)
        #
        # except Exception,e:
        #     print "Could not create proxy "
        #     print "Error was: ",e
        #     sys.exit(1)

    def start(self):
        rospy.init_node('nao_listener')
        for i in range(self.number_of_robots):
            name='to_nao'+str(i+1)
            rospy.Subscriber(name, [String,i+1], self.parse_message)
        rospy.spin()

    def parse_message_1(self, message):
        # # message is json string in the form of:  {'action': 'run_behavior', 'parameters': ["movements/introduction_all_0",...]}
        # # eval the action and run with parameters.
        # # For example, eval result could look like: self,say_text_to_speech(['hello','how are you?'])
        # message = str(message.data)
        # # print("parse_message", message)
        # message_dict = json.loads(message)
        # action = str(message_dict['action'])
        # if 'parameters' in message_dict:
        #     parameters = message_dict['parameters']
        # else:
        #     parameters = ""
        # print("PARSE_MESSAGE")
        # print(str("self." + action + "(1," + str(parameters) + ")"))
        # eval(str("self." + action + "(1," + str(parameters) + ")"))
        print message





# ===== start the program =======
# if len(sys.argv) > 1:
#     nao = NaoNode(sys.argv[1])
# else:
#     nao = NaoNode()


nao = NaoNode(['192','192','192'])

nao.start()