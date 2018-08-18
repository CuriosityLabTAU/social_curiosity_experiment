from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.text import LabelBase
import time
import os
import threading
import rospy
from std_msgs.msg import String,Int32,Int32MultiArray,MultiArrayLayout,MultiArrayDimension
import threading
import json
from random import shuffle, sample
import sys
import datetime
from kivy.uix.dropdown import DropDown





class Config(BoxLayout):
    pass

class Calibration_screen(BoxLayout):
    pass

class Flow(BoxLayout):
    next_button=ObjectProperty()

    pass

class Stop_screen(BoxLayout):
    pass

class ExperimentApp(App):

    subject_id = 0
    state = 0
    proceed = False

    def build(self):
        # connect internal instances of form classes

        self.nao_info = [('192.168.0.102', 'left'), ('192.168.0.106', 'center'), ('192.168.0.101', 'right')]

        self.config = Config()
        self.calibration_screen= Calibration_screen()
        self.flow=Flow()
        self.stop_screen=Stop_screen()


        # defines the screen manager, moves between forms
        self.sm = ScreenManager()

        # connects each form to a screen
        screen = Screen(name='config')
        screen.add_widget(self.config)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='calibration_screen')
        screen.add_widget(self.calibration_screen)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='flow')
        screen.add_widget(self.flow)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)


        screen = Screen(name='stop_screen')
        screen.add_widget(self.stop_screen)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        self.next_step=1
        self.number_of_steps=6

        ###ros
        #roscore
        # t1 = threading.Thread(target=self.worker1)
        # t1.start()
        # threading._sleep(0.2)

        #ros_node
        rospy.init_node('ui')
        self.publisher = rospy.Publisher('the_flow', String, queue_size=10)
        # self.publisher_eye_tracking = rospy.Publisher('eye_tracking', String, queue_size=10)

        #
        self.left_robot_name  ='None'
        self.center_robot_name='None'
        self.right_robot_name ='None'
        self.gender='None'

        return self.sm


    def run_main(self,subject_id, _nao_info):
        str_for_main = ''
        for nao_inst in _nao_info:
            str_for_main = str_for_main + nao_inst[0] + '@' + nao_inst[1] +'@'+ nao_inst[2] + ' '
        #add gender

        str_for_main=str_for_main +self.gender

        os.system('python main.py ' + subject_id + ' ' + str_for_main)

    def start(self,subject_id,nao_ip_center,nao_ip_left,nao_ip_right,experimenter_ip):
        if self.gender=='None':
            return

        self.nao_info = [(nao_ip_left, '0',self.left_robot_name), (nao_ip_center, '1',self.center_robot_name), (nao_ip_right, '2',self.right_robot_name),(experimenter_ip, '3','experimenter')]
        t1 = threading.Thread(target=self.run_main, args=(subject_id, self.nao_info))
        t1.start()
        threading._sleep(25)


        print 'here-ui'


        self.sm.current = "calibration_screen"


    def calibration(self):

        self.sm.current = "flow"


    def run_dynamics(self):
        if self.next_step>self.number_of_steps:
            self.exit_experiment()
            return

        self.next_step+=1

        # if self.next_step <self.number_of_steps:
        #     self.flow.ids['next_button'].text = 'Start Step '+str(self.step)
        # else:
        #     self.flow.ids['next_button'].text = 'End the Experiment'


        if self.next_step -1 ==1:
            self.publisher.publish('alive')
            threading._sleep(1)
            self.publisher.publish('next_step')

        else:
            self.publisher.publish('next_step')




    def looking_at(self,direction):

        self.publisher_eye_tracking.publish(direction)

    def update_robot_name(self,pos,name):
        if pos=='right':
            self.right_robot_name = name

        elif pos=="center":
            self.center_robot_name = name

        elif pos=="left":
            self.left_robot_name = name

    def update_gender(self,_gender):
         self.gender=_gender

    def exit_experiment(self):
        self.publisher.publish('stop')
        self.sm.current = "stop_screen"
        #stop ros bag ~~~~~




    def worker1(self):
        os.system('roscore')

    def btn_released(self,btn,func,param1=None,param2=None,param3=None,param4=None,param5=None):#button configuration
        btn.background_coler=(1,1,1,1)
        if param1 is not None:
            func_param1=param1.text
            if param2 is not None:
                func_param2 = param2.text
                if param3 is not None:
                    func_param3 = param3.text
                    if param4 is not None:
                        func_param4 = param4.text
                        if param5 is not None:
                            func_param5 = param5.text
                            func(func_param1, func_param2, func_param3, func_param4,func_param5)
                        else:
                            func(func_param1, func_param2, func_param3, func_param4)
                    else:
                        func(func_param1, func_param2, func_param3)
                else:
                    func(func_param1,func_param2)

            else:
                func(func_param1)
        else:
            func()

if __name__ == '__main__':
    ExperimentApp().run()

#todo: iu
#todo: basein bhavuer
#todo: stop after bhavuer

