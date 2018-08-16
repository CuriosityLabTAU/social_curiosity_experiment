import numpy as np
from numpy.random import choice
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
        self.position_inv = {'left': 0, 'center': 1 , 'right':2 }


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
        last_robot=int(data.data)
        self.update_next_robot() #finish counting the time


        #process the data and chose the robot that had the most "look time"
        #agregat data
        next_robot_sum=[[],[],[]]
        for v in list(self.next_robot_data):
            self.next_robot_data[v] = -1 * sum(self.next_robot_data[v])
            next_robot_sum[self.position_inv[v]]=self.next_robot_data[v]
        if np.std(self.next_robot_data.values()) <1:
            # if there is no significant one -choose randomly
            robots = [0, 1, 2]

            robot_without_last=robots.remove(last_robot)

            robot_number = choice(robot_without_last)
            chosen_robot = self.position[robot_number]

        else:
            next_robot_sum[last_robot]=0
            chosen_robot=np.argmax(next_robot_sum)

        #restart next_robot_data
        print self.next_robot_data
        self.next_robot_data = {'left': [], 'center': [], 'right': []}

        # print 'next_robot:-=----',next_robot
        # next_robot=str(randint(0, 3))
        # if next_robot=='3':
        #     next_robot='h'
        # print 'mext robot```````````````````:', next_robot

        self.publisher_next.publish(str(chosen_robot))

        # return self.position.keys()[self.position.values().index(chosen_robot)]



start=next_robot()

