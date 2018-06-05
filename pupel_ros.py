from zmq_tools import *

ctx = zmq.Context()
requester = ctx.socket(zmq.REQ)
requester.connect('tcp://localhost:50020') #change ip if using remote machine

requester.send('SUB_PORT')
ipc_sub_port = requester.recv()
monitor = Msg_Receiver(ctx,'tcp://localhost:%s'%ipc_sub_port,topics=('notify.',)) #change ip if using remote machine

while True:
    print(monitor.recv())