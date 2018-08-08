import numpy as np
import time
import rospy
from std_msgs.msg import String
import operator
import sys
import json
import random
import pandas as pd


# from nao_ros import NaoNode
# nao=NaoNode('192.168.0.100','left')


class dynamics():
    def __init__(self,number_of_naos):
        #      |left | center | right |human
        #left  |
        #center|
        #right |

        self.number_of_naos=number_of_naos

        self.interval=0

        self.matrix = np.random.rand(3, 4)

        self.behaviors={0:{
                        "left"  :[{'action':'run_behavior','parameters':['social_curiosity/close_hands']}],
                        "center":[{'action':'run_behavior','parameters':['social_curiosity/close_hands']}],
                        "right" :[{'action':'run_behavior','parameters':['social_curiosity/close_hands']}]},

                        0.125: {
                        "left":   [{'action': 'look_to_other_way', 'parameters': ['left']}],
                        "center": [{'action': 'look_to_other_way', 'parameters': ['center']}],
                        "right":  [{'action': 'look_to_other_way', 'parameters': ['right']}]},

                        0.25: {
                        "left": [{'action': 'disagree'}],
                        "center": [{'action': 'disagree'}],
                        "right": [{'action': 'disagree'}]},


                        0.375:{
                        "left"  :[{'action':'run_behavior','parameters':['social_curiosity/neutral']},{'action': 'move_to_pose', 'parameters': ['left']}],
                        "center":[{'action':'run_behavior','parameters':['social_curiosity/neutral']},{'action': 'move_to_pose', 'parameters': ['center']}],
                        "right" :[{'action':'run_behavior','parameters':['social_curiosity/neutral']},{'action': 'move_to_pose', 'parameters': ['right']}]},

                        0.5: {
                        "left":   [{'action': 'run_behavior', 'parameters': ['social_curiosity/neutral']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity/neutral']}],
                        "right":  [{'action': 'run_behavior', 'parameters': ['social_curiosity/neutral']}]},

                        0.625: {
                        "left":   [{'action': 'move_to_pose', 'parameters': ['left']}],
                        "center": [{'action': 'move_to_pose', 'parameters': ['center']}],
                        "right":  [{'action': 'move_to_pose', 'parameters': ['right']}]},

                        0.75:{
                        "left"  :[{'action':'agree'}],
                        "center":[{'action':'agree'}],
                        "right" :[{'action':'agree'}]},

                        0.875:{
                        "left":   [{'action': 'run_behavior', 'parameters': ['social_curiosity/open_hands']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity/open_hands']}],
                        "right":  [{'action': 'run_behavior', 'parameters': ['social_curiosity/open_hands']}]},

                        1:{
                        "left"  :[{'action': 'run_behavior', 'parameters': ['social_curiosity/left_forward']}],
                        "center":[{'action': 'run_behavior', 'parameters': ['social_curiosity/center_forward']}],
                        "right" :[{'action': 'run_behavior', 'parameters': ['social_curiosity/right_forward']}]}}

        self.discrete_behaviors=self.behaviors.keys()



        self.transformation={0:{1:'left',2:'center','h':'right',},
                             1:{0:'right',2:'left','h':'center'},
                             2:{1:'right',0:'center','h':'left'}}

        self.position={0:'left',1:'center',2:'right'}

        self.next_robot_data={'left':[],'center':[],'right':[]}
        self.present_direction=0

        #ros:
        rospy.init_node('dynamics')
        self.publisher ={}
        self.publisher_alive   ={}
        self.publisher_blinking={}

        for nao in range(number_of_naos):
            name = 'to_nao_' + str(nao)
            print name
            self.publisher[nao]=rospy.Publisher(name, String, queue_size=10)

        #alive & blinking
        for nao in range(number_of_naos):
            name_alive   = 'alive'    + str(nao)
            name_blinking= 'blinking' + str(nao)
            self.publisher_alive[nao]    = rospy.Publisher(name_alive, String, queue_size=10)
            self.publisher_blinking[nao] = rospy.Publisher(name_blinking, String, queue_size=10)


        self.publisher_get_next = rospy.Publisher('get_next', String, queue_size=10)

        rospy.Subscriber('the_flow', String, self.flow_handler)
        rospy.Subscriber('next_robot', String, self.run_dynamics)


        print 'spin '+str(number_of_naos)
        rospy.spin()

    def parse_behavior(self, _dict):
        return json.dumps(_dict)

    def flow_handler(self,data):
        step=data.data

        if step=='alive':
            print 'alive in dynamics'
            for nao in range(self.number_of_naos):
                self.publisher_alive[nao].publish(self.parse_behavior({'action': 'alive'}))
                self.publisher_blinking[nao].publish(self.parse_behavior({'action': 'blinking'}))


        elif step== 'start':
            print step
            self.publisher_get_next.publish(str(0))
            # for nao in range(self.number_of_naos):
            #     self.publisher[nao].publish(self.parse_behavior({'action':'agree'}))

        elif step == 'stop':
            for nao in range(self.number_of_naos):
                self.publisher[nao].publish(self.parse_behavior({'action': 'end_work'}))


    def run_dynamics(self,data):

        print '------'
        secondary_robots=[0,1,2]

        #config robots
        if data.data=='h':
            main_robot = 'h'
        else:
            main_robot=int(data.data)
            secondary_robots.remove(main_robot)

        #main robot - main behavior
        if main_robot!='h':
            self.publisher[main_robot].publish(self.parse_behavior({'action':'run_behavior','parameters':['social_curiosity/talk/1']}))
            self.publisher[main_robot].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(1.0)]}))


        #secondary_robots look at main robot
        for robot in secondary_robots:
            self.publisher[robot].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[robot][main_robot]]}))

        time.sleep(15)

        #secondary_robots look at main behaviour
        if main_robot=='h':
            main_robot=4
        for robot in secondary_robots:
            relationship=self.matrix[robot,main_robot]
            direction_for_behavior=self.transformation[robot][main_robot]
            chosen_behaviour=self.choose_behaviour(relationship)

            behavior=random.choice(self.behaviors[chosen_behaviour][direction_for_behavior])

            self.publisher[robot].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(relationship)]}))
            self.publisher[robot].publish(self.parse_behavior(behavior))

            time.sleep(1)

        time.sleep(5)


        for robot in secondary_robots:
            self.publisher[robot].publish(self.parse_behavior({'action': 'change_current_relationship', 'parameters': [str(-1.0)]}))

        time.sleep(5)

        self.interval+=1

        if self.interval<5:
            self.publisher_get_next.publish(str(self.interval))

        if self.interval==5:
            print self.matrix



    def test(self,aa):
        print 'here'
        self.publisher['left'].publish('{\"action\": \"wake_up\"}')
        # time.sleep(5)

        # self.publisher['left'].publish('{\"action\": \"move_to_pose\", \"parameters\": \"\\\"''right''\\\"\"}')
        # self.publisher['left'].publish('{\"action\": \"look_to_other_way\", \"parameters\": \"\\\"''right''\\\"\"}')
        self.publisher['left'].publish('{\"action\": \"disagree\"}')

        time.sleep(20)

        self.publisher['left'].publish('{\"action\": \"rest\"}')

    def choose_behaviour(self,relationship):
        pick_randomly=np.random.normal(loc=relationship, scale=0.78)
        return min(self.discrete_behaviors, key=lambda x: abs(x - pick_randomly))

        # from numpy.random import choice
        # probability_distribution=[]
        # list_of_candidates=[]
        # draw = np.random.choice(list_of_candidates, 1, p=probability_distribution)
        # return draw

if len(sys.argv) > 1:
    start=dynamics(int(sys.argv[1]))
# else:
#     start=dynamics(1)
    # start.test()
