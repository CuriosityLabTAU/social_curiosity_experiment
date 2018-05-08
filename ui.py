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
from std_msgs.msg import String
import threading
import json
from random import shuffle, sample
import sys
import datetime




class Config(BoxLayout):
    pass
    # nao_ip = ObjectProperty()
    # subject_id= ObjectProperty()

class ExperimentApp(App):

    subject_id = 0
    state = 0
    proceed = False

    def build(self):
        # connect internal instances of form classes

        self.nao_info = [('192.168.0.102', 'left'), ('192.168.0.106', 'center'), ('192.168.0.101', 'right')]

        self.config = Config()

        # defines the screen manager, moves between forms
        self.sm = ScreenManager()

        # connects each form to a screen
        screen = Screen(name='config')
        screen.add_widget(self.config)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        return self.sm

    def run_main(subject_id, _nao_info):
        str_for_main = ''
        for nao_inst in _nao_info:
            str_for_main = str_for_main + nao_inst[0] + '@' + nao_inst[1] + ' '
        os.system('python main.py ' + subject_id + ' ' + str_for_main[:-1])

    def start(self):
        t1 = threading.Thread(target=self.run_main, args=(str(len(self.nao_info)), self.nao_info))
        t1.start()
        threading._sleep(25)

        rospy.init_node('ui')
        publisher = rospy.Publisher('the_flow', String, queue_size=10)

        threading._sleep(5)

        print 'here-ui'
        publisher.publish('60')

        threading._sleep(5)

        print '--'


    def btn_released(self,btn,func,param1=None,param2=None):#button configuration
        btn.background_coler=(1,1,1,1)
        if param1 is not None:
            func_param1=param1.text
            if param2 is not None:
                func_param2 = param2.text
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

