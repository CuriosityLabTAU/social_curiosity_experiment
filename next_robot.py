import numpy as np
import time
import rospy
from std_msgs.msg import String
import operator
import sys
from random import randint



class next_robot():
    def __init__(self):

        self.next_robot_data = {'left': [], 'center': [], 'right': []}
        self.present_direction = 0
        self.position = {0: 'left', 1: 'center', 2: 'right'}

        #ros:
        rospy.init_node('next_robot')

        self.publisher_next=rospy.Publisher('next_robot', String, queue_size=10)

        rospy.Subscriber('get_next', String, self.choose_next_robot)
        rospy.Subscriber('eye_tracking', String, self.update_next_robot)
        rospy.spin()

    def update_next_robot(self,data='None'):

        if data!='None':
            direction=data.data

        else:
            direction = 'None'

        print direction

        if self.present_direction==0:
            if direction== 'None':
                return
            else:
                self.next_robot_data[direction].append(time.time())
                self.present_direction=direction

        else:
            self.next_robot_data[self.present_direction][-1] -= time.time()

            if direction== 'None':
                self.present_direction = 0

            else:
                self.next_robot_data[direction].append(time.time())
                self.present_direction = direction



    def choose_next_robot(self,data):
        self.update_next_robot() #finish counting the time


        # #process the data and chose the robot that had the most "look time"
        # #agregat data
        # for v in list(self.next_robot_data):
        #     self.next_robot_data[v] = -1 * sum(self.next_robot_data[v])
        # if np.std(self.next_robot_data.values()) <1:
        #     # if there is no significant one -choose randomly
        #     robot_number = np.random.random_integers(0, 2)
        #     chosen_robot = self.position[robot_number]
        #
        # else:
        #     chosen_robot=max(self.next_robot_data.iteritems(), key=operator.itemgetter(1))[0]
        #
        # #restart next_robot_data
        # print self.next_robot_data
        # self.next_robot_data = {'left': [], 'center': [], 'right': []}
        #
        # next_robot=str(self.position.keys()[self.position.values().index(chosen_robot)])
        #
        # print 'next_robot:-=----',next_robot
        next_robot=str(randint(0, 2))
        print 'mext robot```````````````````:', next_robot
        self.publisher_next.publish(next_robot)

        # return self.position.keys()[self.position.values().index(chosen_robot)]



start=next_robot()

