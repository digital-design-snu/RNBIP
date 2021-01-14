from multiprocessing import Process, Queue, Value
from ctypes import c_ubyte
import time

tempClk =0
#Clk	= Value(c_ubyte,0)
Clk = Queue(256)

def echoInstAtClock(Clock,instance):
	tempClk =0
	currClk = Clock.get()
	while(currClk < 6):
		currClk = Clock.get()
		if(tempClk != currClk):
			tempClk = currClk
			print(instance)
		
a = Process(target = echoInstAtClock, args = ( Clk,1,))
b = Process(target = echoInstAtClock, args = ( Clk,2,))
c = Process(target = echoInstAtClock, args = ( Clk,3,))
d = Process(target = echoInstAtClock, args = ( Clk,4,))
e = Process(target = echoInstAtClock, args = ( Clk,5,))
f = Process(target = echoInstAtClock, args = ( Clk,6,))

a.start()
b.start()
c.start()
d.start()
e.start()
f.start()

i = 0
while(i<10):
	time.sleep(0.011)
	Clk.put(i)
	i=i+1
	print("---------------------------")
	
a.join()
b.join()
c.join()
d.join()
e.join()
f.join()
	
