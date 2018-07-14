import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import random
import time
import json
import multiprocessing as mp



class NaoSubconscious(object):
    def __init__(self, _robot_ip=str,_node_name=str):
        self.port = 9559
        self.robot_ip=_robot_ip
        self.node_name=_node_name

        #ros:
        rospy.init_node('nao_subconscious'+self.node_name)
        name_publisher ='to_nao_subconscious_'+self.node_name
        name_subscriber='to_nao_'+self.node_name

        self.publisher= rospy.Publisher(name_publisher, String, queue_size=10)

        # self.p = mp.Process(target=self.blinking)
        # self.p.start()
        self.blinking()

        rospy.Subscriber(name_subscriber, String, self.parse_message)
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
        # if action in []:
        self.p.terminate()
        self.p.join()
        self.publisher.publish(message)

    def blinking(self):
        message=self.parse_behavior({'action':'blink'})
        while True:
            self.publisher.publish(message)
            time.sleep(0.5)
            self.publisher.publish(message)
            time.sleep(3.5)



strat=NaoSubconscious(sys.argv[1],sys.argv[2])




