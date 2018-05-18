import numpy as np
import time
import rospy
from std_msgs.msg import String
import sys
import json
import random
from nao_ros import NaoNode
nao=NaoNode('192.168.0.100','left')


class dynamics():
    def __init__(self,number_of_naos):
        #      |left | center | right
        #left  |
        #center|
        #right |

        self.matrix = np.random.random_integers(-1, 1, (3, 3))

        self.behaviors={-1:{
                        "left":['social_curiosity-2ed02f/left_pos'],
                        "center": ['social_curiosity-2ed02f/center_pos'],
                        "right": ['social_curiosity-2ed02f/right_pos']},
                         0:{
                        "left": ['social_curiosity-2ed02f/left_pos'],
                        "center": ['social_curiosity-2ed02f/center_pos'],
                        "right": ['social_curiosity-2ed02f/right_pos']},
                         1:{
                        "left": ['social_curiosity-2ed02f/left_pos'],
                        "center": ['social_curiosity-2ed02f/center_pos'],
                        "right": ['social_curiosity-2ed02f/right_pos']}}

        self.transformation={0:{1:'left',2:'center','h':'right',},
                             1:{0:'right',2:'left','h':'center'},
                             2:{1:'right',0:'center','h':'left'}}

        self.position={0:'left',1:'center',2:'right'}


        #ros:
        rospy.init_node('dynamics')
        self.publisher ={}
        for nao in range(number_of_naos):
            name = 'to_nao_' + self.position[nao]
            print name
            self.publisher[self.position[nao]]=rospy.Publisher(name, String, queue_size=10)

        rospy.Subscriber('the_flow', String, self.test)
        rospy.Subscriber('angles', String, self.parse_angles)
        print 'spin '+str(number_of_naos)
        # rospy.spin()

    def choose_robot(self):
        robots = np.random.random_integers(0, 2, (1, 2))[0]
        if robots[0] == robots[1]:
            robots = self.choose_robot()
        return robots

    def parse_behavior(self, _behavior=str):
        return '{\"action\" : \"run_behavior\", \"parameters\" : [\"' + _behavior[0] + '\", \"wait\"]}'

    def run_dynamics(self,data):
        starttime = time.time()

        time_for_interaction= float(data.data)


        while time.time() -starttime <time_for_interaction:
            robots_for_stemp=self.choose_robot()

            relationship=self.matrix[robots_for_stemp[0],robots_for_stemp[1]]

            side=self.transformation[robots_for_stemp[0]][robots_for_stemp[1]]

            behavior=self.behaviors[relationship][side]

            self.publisher[robots_for_stemp[0]].publish(self.parse_behavior(behavior))
            print behavior,robots_for_stemp[0]

            time.sleep(8)


    def parse_angles(self,data):
        message = str(data.data)

        message_list = json.loads(message)
        actions = message_list[0][0].split(',')

        module = __import__('foo')
        func = getattr(module, actions[2])
        func(int(actions[0]),actions[1],message_list[1])



    def look_to_other_way(self,nao_number,relative_to,angles):
        basepose_HeadYaw = angles[0]
        basepose_HeadPitch = angles[1]

        if relative_to == "right":
            self.publisher[nao_number].publish('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw,HeadPitch;' + str(basepose_HeadYaw + 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08''\\\"\"}')


        elif relative_to == "center":
            sign = random.choice((-1, 1))
            self.publisher[nao_number].publish('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw,HeadPitch;' + str(basepose_HeadYaw + sign * (0.4)) + ',' + str(basepose_HeadPitch + 0.2) + ';0.08''\\\"\"}')

        elif relative_to == "left":
            self.publisher[nao_number].publish('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw,HeadPitch;' + str(basepose_HeadYaw - 1.18) + ',' + str(basepose_HeadPitch - 0.2) + ';0.08''\\\"\"}')


    def test(self):
        print 'here'
        # self.publisher['left'].publish('{\"action\": \"get_angles\", \"parameters\": \"\\\"''left,look_to_other_way''\\\"\"}')
        nao.parse_message('{\"action\": \"get_angles\", \"parameters\": \"\\\"''left,look_to_other_way''\\\"\"}')

if len(sys.argv) > 1:
    start=dynamics(int(sys.argv[1]))
else:
    start=dynamics(1)
    start.test()
