import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import random
import time
import json


class NaoNode():

    def __init__(self, _robot_ip=str,_node_name=str):
        self.port = 9559
        self.robot_ip=_robot_ip
        self.node_name=_node_name
        print 'nao_ros'+_robot_ip

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

        # wake_up

        self.rest()
        #ros:
        rospy.init_node('nao_listener'+self.node_name)
        name='to_nao_'+self.node_name
        self.publisher= rospy.Publisher('angles', String, queue_size=10)
        rospy.Subscriber(name, String, self.parse_message)
        rospy.spin()    #FOR TEST!!!!!!!!!!

    def parse_message(self, message):
        # message is json string in the form of:  {'action': 'run_behavior', 'parameters': ["movements/introduction_all_0",...]}
        # eval the action and run with parameters.
        # For example, eval result could look like: self,say_text_to_speech(['hello','how are you?'])
        message = str(message.data)

        # message = str(message)  #FOR TEST!!!!!!!!!!


        message_dict = json.loads(message)


        action = str(message_dict['action'])
        if 'parameters' in message_dict:
            parameters = message_dict['parameters']
        else:
            parameters = ""
        print(str("self." + action + "(" + str(parameters) + ")"))
        eval(str("self." + action + "(" + str(parameters) + ")"))

    def run_behavior(self, parameters):
        ''' run a behavior installed on nao. parameters is a behavior. For example "movements/introduction_all_0" '''
        try:
            behavior = str(parameters[0])
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
        # print data_str
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
        text=str(parameters)
        # pitch=parameters[1]
        print("say_text_to_animated_speech", text)
        self.animatedSpeech.say(text, {"pitchShift": 1.0})

    def get_angles(self,parameters):
        caller=self.node_name+','+parameters
        names = "Body"
        use_sensors = False
        print("get_angles")
        use_sensors = True
        # string_to_pub = json.dumps([[caller], self.motionProxy.getAngles(names, use_sensors),self.motionProxy.getBodyNames(names)])
        string_to_pub = json.dumps([[caller],self.motionProxy.getAngles(names, use_sensors)])
        print string_to_pub
        self.publisher.publish(string_to_pub)


    def move_to_pose(self,direction):
        direction=direction[0]

        if direction == 'right':
            self.change_pose('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.88,0.01,0.93,0.26,-0.45,-1.2,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,0.0,-0.6,0.0,-1.53,1.41,0.85,0.01,0.96,-0.29,0.53,1.26,-0.05,0.3;0.2')

        elif direction == 'center':
            self.change_pose('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.02,0.2,0.93,0.26,-0.45,-1.21,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,-0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.08')

        elif direction == 'left':
            self.change_pose('HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;0.88,0.01,0.92,0.27,-0.47,-1.22,0.01,0.29,-0.6,0.0,-1.53,1.41,0.84,0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.2')


    def look_to_other_way(self,relative_to):
        relative_to=relative_to[0]


        angles=self.motionProxy.getAngles("Body", True)
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]

        if relative_to == "right":
            self.change_pose('HeadYaw,HeadPitch;' + str(basepose_HeadYaw + 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08')
        elif relative_to == "center":
            sign = random.choice((-1, 1))
            self.change_pose('HeadYaw,HeadPitch;' + str(basepose_HeadYaw + sign * (0.4)) + ',' + str(basepose_HeadPitch + 0.2) + ';0.08')
        elif relative_to == "left":
            self.change_pose('HeadYaw,HeadPitch;' + str(basepose_HeadYaw - 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08')


    def agree(self):
        counter = 0
        angles=self.motionProxy.getAngles("Body", True)
        basepose = angles[1]
        while counter < 3:
            self.change_pose('HeadPitch;' + str(basepose + 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose('HeadPitch;' + str(basepose - 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose('HeadPitch;' + str(basepose) + ';0.08')
            counter += 1

    def disagree(self):
        counter = 0
        angles=self.motionProxy.getAngles("Body", True)
        basepose = angles[0]
        print basepose
        while counter < 3:
            self.change_pose('HeadYaw;' + str(basepose + 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose('HeadYaw;' + str(basepose - 0.2) + ';0.08')
            time.sleep(0.5)
            self.change_pose('HeadYaw;' + str(basepose) + ';0.08')
            counter += 1

strat=NaoNode(sys.argv[1],sys.argv[2])  #FOR TEST!!!!!!!!!!

#
# strat=NaoNode('192.168.0.102','left')  #FOR TEST!!!!!!!!!!


