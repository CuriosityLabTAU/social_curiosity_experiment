import rospy
from std_msgs.msg import String
from nao_ros import NaoNode
import time

nao=NaoNode('192.168.0.100','0')
#
#
# pNames= ['HeadYaw','HeadPitch']
# robot_angles=[0.0,0.0]

def move_to_pose():

    #center
    nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.02,0.2,0.93,0.26,-0.45,-1.21,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,-0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.08''\\\"\"}')

    #right
    # nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;-0.88,0.01,0.93,0.26,-0.45,-1.2,0.01,0.29,-0.6,0.2,-1.53,1.41,0.84,0.0,-0.6,0.0,-1.53,1.41,0.85,0.01,0.96,-0.29,0.53,1.26,-0.05,0.3;0.2''\\\"\"}')

    #left
    # nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw,HeadPitch,LShoulderPitch,LShoulderRoll,LElbowYaw,LElbowRoll,LWristYaw,LHand,LHipYawPitch,LHipRoll,LHipPitch,LKneePitch,LAnklePitch,LAnkleRoll,RHipYawPitch,RHipRoll,RHipPitch,RKneePitch,RAnklePitch,RAnkleRoll,RShoulderPitch,RShoulderRoll,RElbowYaw,RElbowRoll,RWristYaw,RHand;0.88,0.01,0.92,0.27,-0.47,-1.22,0.01,0.29,-0.6,0.0,-1.53,1.41,0.84,0.0,-0.6,-0.2,-1.53,1.41,0.85,0.01,0.96,-0.3,0.53,1.24,-0.04,0.3;0.2''\\\"\"}')

move_to_pose()

def disagree():
    counter = 0
    basepose=nao.get_angles()[0][0]
    print basepose
    while counter <3:
        nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw;'+ str(basepose+0.2)+ ';0.08''\\\"\"}')
        time.sleep(0.5)

        nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw;'+ str(basepose-0.2)+ ';0.08''\\\"\"}')
        time.sleep(0.5)

        counter+=1

    nao.parse_message(        '{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadYaw;' + str(basepose) + ';0.08''\\\"\"}')

def agree():
    counter = 0
    basepose = nao.get_angles()[0][1]
    print basepose
    while counter < 3:
        nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadPitch;' + str(basepose + 0.2) + ';0.08''\\\"\"}')
        time.sleep(0.5)

        nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadPitch;' + str(basepose - 0.2) + ';0.08''\\\"\"}')
        time.sleep(0.5)

        counter += 1

    nao.parse_message('{\"action\": \"change_pose\", \"parameters\": \"\\\"''HeadPitch;' + str(basepose) + ';0.08''\\\"\"}')


def move_other_way(relative_to):





def get_angles_nao():
    a= nao.get_angles()

    angels=''
    names=''
    for ang in a[0]:
        b=round(ang,2)
        angels=angels+','+str(b)

    for nam in a[1]:
        names=names+','+nam

    return names[1:]+';'+angels[1:]
