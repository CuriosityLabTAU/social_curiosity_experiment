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




class Config(BoxLayout):
    pass

class Calibration_screen(BoxLayout):
    pass

class Tracking_screen(BoxLayout):
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
        self.tracking_screen=Tracking_screen()

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

        screen = Screen(name='tracking_screen')
        screen.add_widget(self.tracking_screen)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        # #ros
        # rospy.init_node('ui')
        # self.publisher = rospy.Publisher('the_flow', String, queue_size=10)
        # self.publisher_eye_tracking = rospy.Publisher('eye_tracking', String, queue_size=10)




        return self.sm


    def run_main(self,subject_id, _nao_info):
        str_for_main = ''
        for nao_inst in _nao_info:
            str_for_main = str_for_main + nao_inst[0] + '@' + nao_inst[1] + ' '
        os.system('python main.py ' + subject_id + ' ' + str_for_main[:-1])

    def start(self,subject_id,nao_ip_center,nao_ip_left,nao_ip_right):
        # self.nao_info = [(nao_ip_left, 'left'), (nao_ip_center, 'center'), (nao_ip_right, 'right')]
        # t1 = threading.Thread(target=self.run_main, args=(subject_id, self.nao_info))
        # t1.start()
        # threading._sleep(25)
        #

        #
        # threading._sleep(5)
        #
        # print 'here-ui'
        # self.publisher.publish('60')
        #
        # threading._sleep(5)
        #
        # print '--'

        self.sm.current = "calibration_screen"


    def calibration(self):

        self.sm.current = "tracking_screen"

    def looking_at(self,direction):
        pass
        # self.publisher_eye_tracking.publish(direction)





    def btn_released(self,btn,func,param1=None,param2=None,param3=None,param4=None):#button configuration
        btn.background_coler=(1,1,1,1)
        if param1 is not None:
            func_param1=param1.text
            if param2 is not None:
                func_param2 = param2.text
                if param3 is not None:
                    func_param3 = param3.text
                    if param4 is not None:
                        func_param4 = param4.text
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

