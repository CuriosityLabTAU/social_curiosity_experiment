# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.properties import ObjectProperty
# from kivy.core.window import Window
# from kivy.graphics import Color
# from kivy.uix.widget import Widget
# from kivy.clock import Clock
# from kivy.core.text import LabelBase
# import time
import os
# import threading
import rospy
from std_msgs.msg import String
# import threading
# import json
# from random import shuffle, sample
# import sys
# import datetime
import threading
import time



nao_info=[('192.168.0.102','left'),('192.168.0.106','center'),('192.168.0.101','right')]


def run_main(subject_id,_nao_info):
    str_for_main=''
    for nao_inst in _nao_info:
        str_for_main=str_for_main+nao_inst[0]+'@'+nao_inst[1]+' '
    os.system('python main.py ' + subject_id + ' ' + str_for_main[:-1])


# t1 = threading.Thread(target=run_main, args=('3',nao_info))
# t1.start()
# threading._sleep(25)

rospy.init_node('ui')
publisher = rospy.Publisher ('the_flow', String, queue_size=10)

print 'here-ui'
publisher.publish('60')

print '--'


