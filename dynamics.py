import numpy as np
import time
import rospy
from std_msgs.msg import String


class dynamics():
    def __init__(self,number_of_naos):
        #      |left | center | right
        #left  |
        #center|
        #right |

        self.matrix = np.random.random_integers(-1, 1, (3, 3))

        self.behaviors={-1:{
                        "left":[],
                        "center": [],
                        "right": []  },
                         0:{
                        "left": [],
                        "center": [],
                        "right": []},
                         1:{
                        "left": [],
                        "center": [],
                        "right": []},}

        self.transformation={0:{1:'left',2:'center','h':'right',},
                             1:{0:'right',2:'left','h':'center'},
                             2:{1:'right',0:'center','h':'left'}}

        self.position={0:'left',1:'center',2:'right'}

        self.publisher ={}

        for nao in range(number_of_naos):
            name = 'to_nao' + self.position[nao]
            self.publisher[nao]=rospy.Publisher(name, String, queue_size=10)

    def choose_robot(self):
        robots = np.random.random_integers(0, 2, (1, 2))[0]
        if robots[0] == robots[0]:
            robots = self.choose_robot()
        return robots


    def run_dynamics(self,time_for_interaction=60.0):
        starttime = time.time()


        while time.time() -starttime <time_for_interaction:
            robots_for_stemp=self.choose_robot()

            relationship=self.matrix[robots_for_stemp]

            side=self.transformation[robots_for_stemp[0]][robots_for_stemp[1]]

            behavior=self.behaviors[relationship][side]

            self.publisher[robots_for_stemp[0]].publish(behavior)

            time.sleep(2)
