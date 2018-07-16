import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import random
import time
import json
import numpy as np



class NaoSubconscious():
    def __init__(self, _robot_ip=str,_node_name=str):
        self.port = 9559
        self.robot_ip=_robot_ip
        self.node_name=_node_name

        self.conscious_movement = False

        #ros:
        rospy.init_node('nao_subconscious'+self.node_name)
        name_publisher ='to_nao_subconscious_'+self.node_name
        name_subscriber='to_nao_'+self.node_name
        name_subscriber_alive='alive'+self.node_name


        self.publisher= rospy.Publisher(name_publisher, String, queue_size=10)
        rospy.Subscriber(name_subscriber, String, self.parse_message)
        rospy.Subscriber(name_subscriber_alive, String, self.alive)

        rospy.spin()

    def parse_behavior(self, _dict):
        return json.dumps(_dict)

    def parse_message(self, message):
        # message is json string in the form of:  {'action': 'run_behavior', 'parameters': ["movements/introduction_all_0",...]}
        # eval the action and run with parameters.
        # For example, eval result could look like: self,say_text_to_speech(['hello','how are you?'])
        message = str(message.data)

        message_dict = json.loads(message)

        action = str(message_dict['action'])

        print 'here'

        if action == "natural_motion":
            self.conscious_movement = False

        else:
            self.conscious_movement = True
            self.publisher.publish(message)


    def alive(self,data):
        while True:
            blinking_message = self.parse_behavior({'action': 'blink'})
            if self.conscious_movement == False:
                    self.publisher.publish(blinking_message)
                    time.sleep(0.5)
                    self.publisher.publish(blinking_message)
                    time_now=time.time()
                    time_between_blinks =np.random.exponential(3.5)
                    while self.conscious_movement == False and (time.time()-time_now)<time_between_blinks:  #like sleep
                        pass

strat=NaoSubconscious(sys.argv[1],sys.argv[2])




