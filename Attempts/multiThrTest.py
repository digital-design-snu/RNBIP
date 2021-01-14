import time
from multiprocessing import Process, Queue, Value, Array
from ctypes import c_ubyte

Seed	= Queue()
node1	= Queue()
node2	= Queue()
node3	= Queue()
node4	= Queue()
node5	= Queue()
end		= Queue()

#a loop variable update simulation

def unit1(read,write):
	write.put(read.get())
		
Pnode1 = Process(target = unti1 , args = (Seed,node1,))
Pnode2 = Process(target = unti1 , args = (node1,node2,))
Pnode3 = Process(target = unti1 , args = (node2,node3,))
Pnode4 = Process(target = unti1 , args = (node3,node4,))
Pnode5 = Process(target = unti1 , args = (node4,node5,))
Pnode6 = Process(target = unti1 , args = (node5,end,))

# starting threads

Pnode1.start()
Pnode2.start()
Pnode3.start()
Pnode4.start()
Pnode5.start()
Pnode6.start()

Pnode1.join()
Pnode2.join()
Pnode3.join()
Pnode4.join()
Pnode5.join()
Pnode6.join()

