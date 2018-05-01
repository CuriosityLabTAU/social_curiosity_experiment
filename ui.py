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
# import rospy
# from std_msgs.msg import String
# import threading
# import json
# from random import shuffle, sample
# import sys
# import datetime

nao_info=[('192.168.0.100','left'),('192.168.0.100','center')]



def run_main(subject_id,_nao_info):
    str_for_main=''
    for nao_inst in _nao_info:
        str_for_main=str_for_main+nao_inst[0]+'@'+nao_inst[1]+' '
    os.system('python main.py ' + subject_id + ' ' + str_for_main[:-1])



run_main('3',nao_info)


#====
# class dynamics():
# function: robot1, robot2, friends[-1, 0, 1] ==> do behavior

# matrix = None

# run_dynamics:
# -go over time steps
# --- choose one item in the matrix --> robot1, robot2, friendship
# --- do behavior
