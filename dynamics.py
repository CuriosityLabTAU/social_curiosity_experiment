import numpy as np
import time
import rospy
from std_msgs.msg import String
import operator
import sys
import json
import random



# from nao_ros import NaoNode
# nao=NaoNode('192.168.0.100','left')


class dynamics():
    def __init__(self,number_of_naos):
        #      |left | center | right
        #left  |
        #center|
        #right |

        self.number_of_naos=number_of_naos

        self.interval=0

        self.matrix = np.random.random_integers(-1, 1, (3, 3))

        self.behaviors={-1:{
                        "left"  :[{'action':'disagree'},{'action':'look_to_other_way','parameters':['left']},{'action':'run_behavior','parameters':['social_curiosity/close_hands']}],
                        "center":[{'action':'disagree'},{'action':'look_to_other_way','parameters':['center']},{'action':'run_behavior','parameters':['social_curiosity/close_hands']}],
                        "right" :[{'action':'disagree'},{'action':'look_to_other_way','parameters':['right']},{'action':'run_behavior','parameters':['social_curiosity/close_hands']}]},

                         0:{
                        "left"  :[{'action':'run_behavior','parameters':['social_curiosity/neutral']},{'action': 'move_to_pose', 'parameters': ['left']}],
                        "center":[{'action':'run_behavior','parameters':['social_curiosity/neutral']},{'action': 'move_to_pose', 'parameters': ['center']}],
                        "right" :[{'action':'run_behavior','parameters':['social_curiosity/neutral']},{'action': 'move_to_pose', 'parameters': ['right']}]},

                         1:{
                        "left"  :[{'action':'agree'},{'action':'run_behavior','parameters':['social_curiosity/open_hands']},{'action':'run_behavior','parameters':['social_curiosity/left_forward']}],
                        "center":[{'action':'agree'},{'action':'run_behavior','parameters':['social_curiosity/open_hands']},{'action':'run_behavior','parameters':['social_curiosity/center_forward']}],
                        "right" :[{'action':'agree'},{'action':'run_behavior','parameters':['social_curiosity/open_hands']},{'action':'run_behavior','parameters':['social_curiosity/right_forward']}]}}

        self.transformation={0:{1:'left',2:'center','h':'right',},
                             1:{0:'right',2:'left','h':'center'},
                             2:{1:'right',0:'center','h':'left'}}

        self.position={0:'left',1:'center',2:'right'}

        self.next_robot_data={'left':[],'center':[],'right':[]}
        self.present_direction=0

        #ros:
        rospy.init_node('dynamics')
        self.publisher ={}
        self.publisher_alive ={}

        for nao in range(number_of_naos):
            name = 'to_nao_' + str(nao)
            print name
            self.publisher[nao]=rospy.Publisher(name, String, queue_size=10)

        #alive
        for nao in range(number_of_naos):
            name = 'alive' + str(nao)
            print name
            self.publisher_alive[nao] = rospy.Publisher(name, String, queue_size=10)

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
            for nao in range(self.number_of_naos):
                self.publisher_alive[nao].publish(self.parse_behavior({'action': 'alive'}))

        elif step== 'start':
            print step
            self.publisher_get_next.publish(str(0))



    def run_dynamics(self,data):

        print '------'
        secondary_robots=[0,1,2]

        #config robots
        main_robot=int(data.data)
        secondary_robots.remove(main_robot)

        #main robot - main behavior
        self.publisher[main_robot].publish(self.parse_behavior({'action':'run_behavior','parameters':['social_curiosity/talk/1']}))

        #secondary_robots look at main robot
        for robot in secondary_robots:
            self.publisher[robot].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': [self.transformation[robot][main_robot]]}))

        time.sleep(15)

        #secondary_robots look at main behaviour
        for robot in secondary_robots:
            relationship=self.matrix[robot,main_robot]
            direction_for_behavior=self.transformation[robot][main_robot]
            behavior=random.choice(self.behaviors[relationship][direction_for_behavior])

            self.publisher[robot].publish(self.parse_behavior(behavior))

        time.sleep(10)



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


if len(sys.argv) > 1:
    start=dynamics(int(sys.argv[1]))
# else:
#     start=dynamics(1)
    # start.test()
