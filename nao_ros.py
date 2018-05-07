import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
# import almath
import time
import datetime
import json


class NaoNode():

    def __init__(self, _robot_ip=str,_node_name=str):
        self.port = 9559
        self.robot_ip=_robot_ip
        self.node_name=_node_name

        try:
            #motionProxy
            self.motionProxy  = ALProxy("ALMotion", self.robot_ip, self.port)

            # postureProxy
            self.postureProxy = ALProxy("ALRobotPosture", self.robot_ip, self.port)

            # animatedSpeech
            self.animatedSpeech = ALProxy("ALAnimatedSpeech", self.robot_ip, self.port)

            # managerProxy
            self.managerProxy = ALProxy("ALBehaviorManager", self.robot_ip, self.port)

            #texttospeech
            self.tts = ALProxy("ALTextToSpeech", self.robot_ip, self.port)

            #trackerProxy
            self.trackerProxy = ALProxy("ALTracker", self.robot_ip, self.port)

        except Exception,e:
            print "Could not create proxy "
            print "Error was: ",e
            sys.exit(1)

        #ros:
        rospy.init_node('nao_listener'+self.node_name)
        name='to_nao'+self.node_name
        rospy.Subscriber(name, String, self.parse_message)
        rospy.spin()

    def parse_message(self, message):
        # message is json string in the form of:  {'action': 'run_behavior', 'parameters': ["movements/introduction_all_0",...]}
        # eval the action and run with parameters.
        # For example, eval result could look like: self,say_text_to_speech(['hello','how are you?'])
        message = str(message.data)
        # print("parse_message", message)
        message_dict = json.loads(message)
        action = str(message_dict['action'])
        if 'parameters' in message_dict:
            parameters = message_dict['parameters']
        else:
            parameters = ""
        print("PARSE_MESSAGE")
        print(str("self." + action + "(" + str(parameters) + ")"))
        eval(str("self." + action + "(" + str(parameters) + ")"))

    def run_behavior(self, parameters):
        ''' run a behavior installed on nao. parameters is a behavior. For example "movements/introduction_all_0" '''
        try:
            behavior = str(parameters[0])
            print("behavior",behavior)
            if len(parameters) > 1:
                if parameters[1] == 'wait':
                    self.managerProxy.runBehavior(behavior)

                else:
                    self.managerProxy.post.runBehavior(behavior)
            else:
                self.managerProxy.post.runBehavior(behavior)

        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e


    def say_text_to_speech (self, parameters):
        # make nao say the string text
        # parameters in the form of ['say something','say something','say something']
        for text in parameters:
            print("say_text_to_speech", text)
            self.tts.say (str(text))

    def rest(self):
        self.motionProxy.rest()

    def wake_up(self):
        self.motionProxy.wakeUp()

    def open_hand(self, parameters):
        print('open_hand', parameters)
        hand_name = parameters[0]
        self.motionProxy.openHand('RHand')

    def look_at(self, parameters):
        vect2 = parameters[0]
        fractionmaxspeed = parameters[1]
        use = parameters[2]
        self.trackerProxy.lookAt(vect2, fractionmaxspeed, use)

    def point_at(self,parameters):
        print('pointAt', parameters)
        effector = 'RArm'
        vect = parameters[0]
        fractionmaxspeed = parameters[1]
        use = parameters[2]
        self.trackerProxy.pointAt(effector, vect, fractionmaxspeed, use)

    def change_pose(self, data_str):
        # data_str = 'name1, name2;target1, target2;pMaxSpeedFraction'
        info = data_str.split(';')
        pNames = info[0].split(',')
        pTargetAngles = [float(x) for x in info[1].split(',')]
        # pTargetAngles = [x * almath.TO_RAD for x in pTargetAngles]  # Convert to radians
        pMaxSpeedFraction = float(info[2])
        # print(pNames, pTargetAngles, pMaxSpeedFraction)
        self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    def animated_speech(self,parameters):
        # make nao say the string text
        # parameters in the form of ['say something',pitchShift=float]
        text=parameters[0]
        pitch=parameters[1]
        print("say_text_to_animated_speech", text)
        self.animatedSpeech.say(text, {"pitchShift": pitch})

strat=NaoNode(sys.argv[1],sys.argv[2])