import os
import threading
import time
import sys
from nao_ros import NaoNode


def intro(subject_id=0, nao_info=['192.168.0.100','1']):
    #nao_info is a list of [nao_ip,nao_name]
    start_working(subject_id, nao_info)


    time.sleep(60)


def start_working(subject_id, nao_info):

    #make the class instance for nao_ros
    def worker1(_nao):
        start_nao=NaoNode(_nao[0],_nao[1])

    # def worker1():
    #     os.system('roslaunch multi_camera_affdex multi_camera_affdex.launch')
    #
    # def worker2():
    #     os.system('roslaunch skeleton_markers markers.launch')
    #     return
    #
    # def worker3():
    #     os.system('python curious_game/angle_matrix.py')
    #     return
    #
    # def worker6():
    #     os.system('rosbag record -a -o data/physical_curiosity_big_experiment_' + str(subject_id) + '.bag')
    #
    # def worker7():
    #     os.system('python curious_game/skeleton_angles.py')


    for nao in nao_info:
        t1 = threading.Thread(target=worker1,args=(nao,))
        t1.start()
        threading._sleep(2.5)

    # t2 = threading.Thread(target=worker2)
    # t2.start()
    # threading._sleep(0.2)
    #
    # t3 = threading.Thread(target=worker3)
    # t3.start()
    # threading._sleep(0.2)
    #
    # t4 = threading.Thread(target=worker4)
    # t4.start()
    # threading._sleep(0.2)
    #
    # t5 = threading.Thread(target=worker5)
    # t5.start()
    # threading._sleep(0.2)
    #
    # t6 = threading.Thread(target=worker6)
    # t6.start()
    # threading._sleep(0.2)
    #
    # t7 = threading.Thread(target=worker7)
    # t7.start()
    # threading._sleep(0.2)

if len(sys.argv) > 1:
    print('sys.argv', sys.argv)
    nao_arg_list=[element.split('@') for element in sys.argv[2:]]
    intro(int(sys.argv[1]), nao_arg_list)
else:
    intro()
