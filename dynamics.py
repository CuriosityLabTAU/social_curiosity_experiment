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


# from nao_ros import NaoNode
# nao=NaoNode('192.168.0.100','left')


class dynamics():
    def __init__(self,number_of_naos):
        #      |left | center | right |human
        #left  |
        #center|
        #right |

        self.experimenter_nao=3

        self.number_of_naos=number_of_naos

        self.experiment_step=0

        self.interval=0

        self.matrix = self.bin_matrix(np.random.rand(3, 4))

        self.behaviors={0:{
                        "left"  :[{'action':'run_behavior','parameters':['social_curiosity/close_hands']}],
                        "center":[{'action':'run_behavior','parameters':['social_curiosity/close_hands']}],
                        "right" :[{'action':'run_behavior','parameters':['social_curiosity/close_hands']}]},

                        1: {
                        "left":   [{'action': 'look_to_other_way', 'parameters': ['left']}],
                        "center": [{'action': 'look_to_other_way', 'parameters': ['center']}],
                        "right":  [{'action': 'look_to_other_way', 'parameters': ['right']}]},

                        2: {
                        "left": [{'action': 'disagree'}],
                        "center": [{'action': 'disagree'}],
                        "right": [{'action': 'disagree'}]},

                        3: {
                        "left":   [{'action': 'run_behavior', 'parameters': ['social_curiosity/neutral']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity/neutral']}],
                        "right":  [{'action': 'run_behavior', 'parameters': ['social_curiosity/neutral']}]},

                        4: {
                        "left":   [{'action': 'move_to_pose', 'parameters': ['left']}],
                        "center": [{'action': 'move_to_pose', 'parameters': ['center']}],
                        "right":  [{'action': 'move_to_pose', 'parameters': ['right']}]},

                        5:{
                        "left"  :[{'action':'agree'}],
                        "center":[{'action':'agree'}],
                        "right" :[{'action':'agree'}]},

                        6:{
                        "left":   [{'action': 'run_behavior', 'parameters': ['social_curiosity/open_hands']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['social_curiosity/open_hands']}],
                        "right":  [{'action': 'run_behavior', 'parameters': ['social_curiosity/open_hands']}]},

                        7:{
                        "left"  :[{'action': 'run_behavior', 'parameters': ['social_curiosity/right_forward']}],
                        "center":[{'action': 'run_behavior', 'parameters': ['social_curiosity/center_forward']}],
                        "right" :[{'action': 'run_behavior', 'parameters': ['social_curiosity/left_forward']}]},

                        8:{
                        "left": [{'action': 'run_behavior', 'parameters': ['elina_julia/hate_left']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['elina_julia/hate_center']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['elina_julia/hate_center']}]},

                        9:{
                        "left": [{'action': 'run_behavior', 'parameters': ['elina_julia/right_hand_behind_head_left']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['elina_julia/left_hand_behind_head_center']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['elina_julia/left_hand_behind_head_right']}]},

                        10:{
                        "left": [{'action': 'run_behavior', 'parameters': ['elina_julia/left_lean_back']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['elina_julia/center_hand_lean_forward']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['elina_julia/right_lean_back']}]},

                        11:{
                        "left": [{'action': 'run_behavior', 'parameters': ['elina_julia/left_hand_random']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['elina_julia/right_hand_random']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['elina_julia/right_hand_random']}]},

                        12:{
                        "left": [{'action': 'run_behavior', 'parameters': ['elina_julia/right_hand_random']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['elina_julia/left_hand_random']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['elina_julia/left_hand_random']}]},

                        13:{
                        "left": [{'action': 'run_behavior', 'parameters': ['elina_julia/hate_2']}],
                        "center": [{'action': 'run_behavior', 'parameters': ['elina_julia/hate_2']}],
                        "right": [{'action': 'run_behavior', 'parameters': ['elina_julia/hate_2']}]},

                        14:{
                        "left":   [{'action':'look_down'}],
                        "center": [{'action':'look_down'}],
                        "right":  [{'action':'look_down'}]}}

        self.metadata_for_experiment_steps = {
                                        0: {'matrix':self.bin_matrix(np.random.rand(3, 4)),
                                            'turns' :['0','1','2','h''0','1','2','h'],
                                            'question_time':False,
                                            'experimenter_before':None,
                                            'experimenter_after' : None},

                                        1: {'matrix': self.bin_matrix(np.random.rand(3, 4)),
                                            'turns': ['0', '1', '2', 'h''0', '1', '2', 'h'],
                                            'question_time': False,
                                            'experimenter_before': [['action',time]],
                                            'experimenter_after': None},

                                        2: {'matrix': self.bin_matrix(np.random.rand(3, 4)),
                                            'turns': ['0', '1', '2', 'h''0', '1', '2', 'h']},

                                        3: {'matrix': self.bin_matrix(np.random.rand(3, 4)),
                                            'turns': ['0', '1', '2', 'h''0', '1', '2', 'h']},

                                        4: {'matrix': self.bin_matrix(np.random.rand(3, 4)),
                                            'turns': ['0', '1', '2', 'h''0', '1', '2', 'h']},

                                        5: {'matrix': self.bin_matrix(np.random.rand(3, 4)),
                                            'turns': ['0', '1', '2', 'h''0', '1', '2', 'h']}}

        self.discrete_behaviors=sorted(self.behaviors.keys())

        self.probs_from_AMT = pd.read_csv('probs_from_AMT.csv')

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
            print data.data
            main_robot=int(data.data)
            secondary_robots.remove(main_robot)

        #main robot - main behavior
        if main_robot!='h':
            self.publisher[main_robot].publish(self.parse_behavior({'action':'run_behavior','parameters':['social_curiosity/talk/1']}))
            self.publisher[main_robot].publish(self.parse_behavior({'action':'change_current_relationship','parameters':[str(1.0)]}))


        #secondary_robots look at main robot
        for robot in secondary_robots:
            time.sleep(1.1)
            self.publisher[robot].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[robot][main_robot]]}))


        time.sleep(8)

        #secondary_robots look at main behaviour
        if main_robot=='h':
            place_in_matrix=4
        else:
            place_in_matrix=main_robot

        for robot in secondary_robots:
            relationship=self.matrix[robot,place_in_matrix]
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


    def run_dynamics_for_AMT(self, data):
        robots = [0, 1]


        for i in range(15):

            # # secondary_robots look at main robot
            # self.publisher[0].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[0][1]]}))
            # time.sleep(1.5)
            #
            # self.publisher[1].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[1][0]]}))

            time.sleep(3)


            direction_for_behavior = self.transformation[1][0]

            behavior = self.behaviors[i][direction_for_behavior][0]
            # self.publisher[1].publish(self.parse_behavior(behavior))
            self.publisher[1].publish(self.parse_behavior({'action': 'look_up'}))


            print i

            time.sleep(6)

            self.publisher[0].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[0][2]]}))
            time.sleep(1.5)
            self.publisher[1].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[1]['h']]}))

            time.sleep(8)


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
        probability_distribution=self.probs_from_AMT[str(relationship)].tolist()
        list_of_candidates=self.discrete_behaviors
        draw = np.random.choice(list_of_candidates, 1, p=probability_distribution)
        return draw[0]

    def bin_matrix(self,_matrix):
        number_of_bins = 9
        bins = [i * (1.0 / number_of_bins) for i in xrange(number_of_bins + 1)]
        labels = [(bins[i] + bins[i + 1]) / 2.0 for i in xrange(number_of_bins)]
        labels = list(np.around(np.array(labels), 3))
        matrix=_matrix

        for i in range(_matrix.shape[0]):
            for j in range(_matrix.shape[1]):
                for _bin in range(len(bins) - 1):
                    if matrix[i, j] >= bins[_bin] and matrix[i, j] < bins[_bin + 1]:
                       matrix[i, j] = labels[_bin]
        return matrix

if len(sys.argv) > 1:
    start=dynamics(int(sys.argv[1]))
# else:
#     start=dynamics(1)
    # start.test()
