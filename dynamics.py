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

        self.matrix = np.random.random_integers(-1, 1, (3, 3))

        self.behaviors={-1:{
                        "left"  :[{'action':'disagree'},{'action':'look_to_other_way'},{'action':'run_behavior','parameters':'social_curiosity/close_hands'}],
                        "center":[{'action':'disagree'},{'action':'look_to_other_way'},{'action':'run_behavior','parameters':'social_curiosity/close_hands'}],
                        "right" :[{'action':'disagree'},{'action':'look_to_other_way'},{'action':'run_behavior','parameters':'social_curiosity/close_hands'}]},

                         0:{
                        "left"  :['social_curiosity-2ed02f/left_pos'],
                        "center":['social_curiosity-2ed02f/center_pos'],
                        "right" :['social_curiosity-2ed02f/right_pos']},

                         1:{
                        "left"  :['social_curiosity-2ed02f/left_pos'],
                        "center":['social_curiosity-2ed02f/center_pos'],
                        "right" :['social_curiosity-2ed02f/right_pos']}}

        self.transformation={0:{1:'left',2:'center','h':'right',},
                             1:{0:'right',2:'left','h':'center'},
                             2:{1:'right',0:'center','h':'left'}}

        self.position={0:'left',1:'center',2:'right'}

        self.next_robot_data={'left':[],'center':[],'right':[]}
        self.present_direction=0

        #ros:
        rospy.init_node('dynamics')
        self.publisher ={}
        for nao in range(number_of_naos):
            name = 'to_nao_' + str(nao)
            print name
            self.publisher[nao]=rospy.Publisher(name, String, queue_size=10)

        rospy.Subscriber('the_flow', String, self.run_dynamics)
        rospy.Subscriber('eye_tracking', String, self.update_next_robot)

        print 'spin '+str(number_of_naos)
        rospy.spin()

    def parse_behavior(self, _dict):
        return json.dumps(_dict)


    def run_dynamics(self,data):

        while True:
            secondary_robots=[0,1,2]

            #config robots
            main_robot=self.choose_next_robot()
            secondary_robots.remove(main_robot)

            #main robot - main behavior
            self.publisher[main_robot].publish(self.parse_behavior({'action':'run_behavior','parameters':'social_curiosity/talk/1'}))

            #secondary_robots look at main robot
            for robot in secondary_robots:
                self.publisher[robot].publish(self.parse_behavior({'action': 'move_to_pose', 'parameters': self.transformation[robot][main_robot]}))

            time.sleep(7)

            #secondary_robots look at main behaviour
            for robot in secondary_robots:
                relationship=self.matrix[robot,main_robot]
                direction_for_behavior=self.transformation[robot][main_robot]
                behavior=random.choice(self.behaviors[relationship][direction_for_behavior])

                self.publisher[robot].publish(self.parse_behavior(behavior))

            time.sleep(15)


    def update_next_robot(self,data='None'):
        direction=data.data
        if self.present_direction==0:
            if direction== 'None':
                return
            else:
                self.next_robot_data[direction].append(time.time())

        else:
            self.next_robot_data[self.present_direction][-1] -= time.time()

            if direction== 'None':
                self.present_direction = 0

            else:
                self.present_direction = direction

    def choose_next_robot(self):
        self.update_next_robot() #finish counting the time

        #process the data and chose the robot that had the most "look time"
        #agregat data
        for v in list(self.next_robot_data):
            self.next_robot_data[v] = -1 * sum(self.next_robot_data[v])
        if np.std(self.next_robot_data.values()) <1:
            # if there is no significant one -choose randomly
            robot_number = np.random.random_integers(0, 2)
            chosen_robot = self.position[robot_number]

        else:
            chosen_robot=max(self.next_robot_data.iteritems(), key=operator.itemgetter(1))[0]

        #restart next_robot_data
        self.next_robot_data = {'left': [], 'center': [], 'right': []}

        return self.position.keys()[self.position.values().index(chosen_robot)]


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
else:
    start=dynamics(1)
    # start.test()
