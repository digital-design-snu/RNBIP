import time
from multiprocessing import Process,Value,Queue,Array,Barrier
# Block Design
# process declarition with all shared variables
# Procces tasks on current mmachine state
#process essentially creates a copy of all write affect control bits for that cycle # Write schedule protect
# Process state is recorded :D # essentially as an outcome of the previous state
# process Wait at Barrier for Synchronous
# Process executes Synchronous functions
# All mem writes are performed prep for next set of control siglanls is done
# wait for Kill Signal 
# barrier 2
#repeat

def hi():
	print("Hello this is samuel the donkey at barrier 1")
	return

def hi2():
	print("Hello this is samuel the donkey at barrier 2")
	return

def Proc(q1,q2,b1,b2):	
	a = q1.get()+1
	q2.put(a)
	print(a)
	b1.wait()
	a = q1.get()+1
	q2.put(a)
	print(a)
	print(b2.n_waiting)
	b2.wait()
	return  


Q1 = Queue()
Q2 = Queue()
Q3 = Queue()
Q4 = Queue()
Q5 = Queue()

b1 = Barrier(5,action = hi)
b2 = Barrier(5,action = hi2)

P1 = Process(target=Proc , args=(Q1,Q2,b1,b2,))
P2 = Process(target=Proc , args=(Q2,Q3,b1,b2,))
P3 = Process(target=Proc , args=(Q3,Q4,b1,b2,))
P4 = Process(target=Proc , args=(Q4,Q5,b1,b2,))

P1.start()
P2.start()
P3.start()
P4.start()


Q1.put(10)
b1.wait()
print(Q5.get())
Q1.put(100)
b2.wait()
print(Q5.get())

P1.join()
P2.join()
P3.join()
P4.join()

