#
#
#
# import pandas as pd
#
# AMT_data=pd.read_csv('AMT_demo.csv')
# print AMT_data


import sh
#

#
# for num in range(10,40):
#     ip = "192.168.0."+str(num)
#
#     try:
#         sh.ping(ip, "-c 1",_out="/dev/null")
#         print "PING ",ip , "OK"
#     except sh.ErrorReturnCode_1:
#         print "PING ", ip, "FAILED"
import os
os.system('NetResView.exe /DisplayComputers 1 /RetrieveIPAddresses /stext ipfile')
my_file = open('ipfile')
for line in my_file :
    print my_file.readline()