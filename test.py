import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import random
import time
import json
import multiprocessing as mp
import time

class NaoNode(object):
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

            #AutonomousLife
            self.autonomous = ALProxy("ALAutonomousLife", self.robot_ip, self.port)

            # PostureProxy
            self.postureProxy = ALProxy("ALRobotPosture", self.robot_ip, 9559)


            #LEDS Api:

            self.leds = ALProxy("ALLeds", self.robot_ip, self.port)
            names1 = ["FaceLed0", "FaceLed4"]
            names2 = ["FaceLed1", "FaceLed3", "FaceLed5", "FaceLed7"]
            names3 = ["FaceLed2", "FaceLed6"]

            self.leds.createGroup("leds1", names1)
            self.leds.createGroup("leds3", names3)
            self.leds.createGroup("leds2", names2)


        except Exception,e:
            print "Could not create proxy "
            print "Error was: ",e
            sys.exit(1)


        # autonomous_state
        # self.set_autonomous_state_off()

        # wake_up
        self.wake_up()

        # Sitdown
        # self.postureProxy.goToPosture("Sit", 1.0)

        # wake_up
        # self.rest()


    def set_autonomous_state_off(self):
        # put nao in autonomous state
        # parameters in the form of ['solitary','disabled']
        # http://doc.aldebaran.com/2-1/naoqi/core/autonomouslife.html
        self.autonomous.setState('disabled')

    def rest(self):
        self.motionProxy.rest()

    def wake_up(self):
        self.motionProxy.wakeUp()

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

    def blink(self):
        print 'here'
        self.leds.off("leds1")
        self.leds.off("leds2")
        self.leds.off("leds3")
        self.leds.on("leds3")
        self.leds.on("leds2")
        self.leds.on("leds1")

    def blinking(self):
        while True:
            self.blink()
            time.sleep(0.5)
            self.blink()
            time.sleep(3.5)

    def run(self):
        p = mp.Process(target=self.blinking)
        p.start()
        time.sleep(10)
        p.terminate()
        p.join()
        print 'main process exiting..'

a = NaoNode('192.168.0.101','ss')
a.run()