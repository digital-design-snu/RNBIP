##------------------------------------------------------------------------------ 
#                     			  The RNBIP
#							Visualisation Encoder
#								aka. Voyager
#                     This Multi threaded module 1:1 emulates
# 					 The operation of the RNBIP Micro-Controller
#						Author :: @CommandPaul ( Paul George )
#							  Junior Year 2016-17
#							 Shiv Nadar University
##------------------------------------------------------------------------------

##	This Python Script is hierarchially seperated into the original modulles of
##	the architecture , all original signals have been preserved the encoded data
##	can be visualised in VedantCJ (Vedant Chakravarty`s) Visualisation module 
## 	Developed in C++ using the QT Framework , The input to this file should be 
## 	in the format output by the Pn337(Prasanna Natarajan) Assembler . 

#---- Fixit Comments Remove from final

#1 :: put something to make sure regissters overflow at 8 bits :P
#2 :: put an exit condition checker in the loop :P
#---- End of Fixit Comments

#	the killthr flag is negative logic 

#	Import Libraries

import time
from multiprocessing import Process,Value,Queue,Array,Barrier
from ctypes import c_ubyte,c_char

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
'''def Proc(q1,q2,b1,b2):	
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
'''
#repeat

def PrintState(): # data bus being a waited signal is printed as valoutput of module with an output enabled 
	#Barrier1 = Barrier(5,action = PrintState)
	print("Hello this is samuel the donkey at barrier 2")
	return


def MemoryModule(ControlBits,ProgramCounter,RegisterArray,StackPointer,DataBus,Memory,Kill,Barrier1,Barrier2):	
	#initialisation read from file			
	counter=0
	MEMConfFile = open('machCode.bin')
	while(counter<256):
		line = MEMConfFile.readline()
		Memory[counter] = (int(line,2))
		counter = counter+1	
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		WR = ControlBits[1] #cached for Synchronous Protection
		if(ControlBits[2]== '1'): address = ProgramCounter.value
		elif(ControlBits[3]== '1'): address = StackPointer.value
		else: address = RegisterArray[0] 
		if(ControlBits[0] == '1'):
			DataBus.put(Memory[address])
		Barrier1.wait()
		# Synchronous Here after
		if( WR == '1'):
			Memory[address] = DataBus.get() #value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill.value == 1 ): return
	return

def ProgramCounterModule(ControlBits,ProgramCounter,OperandRegister,DataBus,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	ProgramCounter.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LPC = ControlBits[6] #cached for Synchronous Protection
		IPC = ControlBits[5] #cached for Synchronous Protection
		if(ControlBits[4] == '1'):
			DataBus.put(ProgramCounter.value)
		Barrier1.wait()
		# Synchronous Here after
		if( LPC == '1' and IPC == '0' ):
			ProgramCounter.value = DataBus.get() # .value requirement ? Not Required :)
		elif( LPC == '0' and IPC == '1'):
			ProgramCounter.value = ProgramCounter.value + 1  # .value requirement ? Not Required :)
		elif( LPC == '1' and IPC == '1'):
			ProgramCounter.value = OperandRegister  # .value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill == 1 ): return
	return

def IOModule(ControlBits,IO_In,IO_Out,DataBus,RegSel,Kill,Barrier1,Barrier2):
	#initialisation
	IO_In  = [0,0,0,0,0,0,0,0]
	IO_Out = [0,0,0,0,0,0,0,0]
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LOP = ControlBits[14] #cached for Synchronous Protection
		REGSEL = RegSel.value #cached for Synchronous Protection
		if(ControlBits[13] == '1'):
			DataBus.put(IO_In[RegSel.value])
		Barrier1.wait()
		# Synchronous Here after
		if( LOP == '1'):
			IO_Out[REGSEL] = DataBus.get() # .value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill == 1 ): return
	return

	
def OperandRegisterModule(ControlBits,OperandRegister,DataBus,Kill,Barrier1,Barrier2):
	#initialisation
	OperandRegister.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LOR = ControlBits[16] #cached for Synchronous Protection
		if(ControlBits[15] == '1'):
			DataBus.put(OperandRegister.value)
		Barrier1.wait()
		# Synchronous Here after
		if( LOR == '1'):
			OperandRegister.value = DataBus.get() # .value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill == 1 ): return
	return

def ALU_Module(ControlBits,DataBus,OperandRegister,AluOpcode,CarryIn,AluOut,FlagRegister,Kill,Barrier1,Barrier2):
	#initialisation
	OperandRegister.value = 0
	ALU_imOut = 0 
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		SAL = ControlBits[17] #cached for Synchronous Protection
		OpCode = AluOpcode.value #for faster Switch below :|
		if(SAL == '1'):
			dataBus = DataBus.get()
			if   (OpCode == 0    ):  ALU_imOut = 0                            
			else :
				dataBus = DataBus.get()
				OperandReg = OperandRegister.value
				if   (OpCode == 1    ):  ALU_imOut = dataBus                
				elif (OpCode == 2    ):  ALU_imOut = (~dataBus & 0xFF)          
				elif (OpCode == 3    ):  ALU_imOut = OperandReg                          
				elif (OpCode == 4    ):  ALU_imOut = dataBus+1                  
				elif (OpCode == 5    ):  ALU_imOut = dataBus-1                  
				elif (OpCode == 6    ):  ALU_imOut = (dataBus<<1+Cin)           
				elif (OpCode == 7    ):  ALU_imOut = (((dataBus%2)<<8)+(Cin<<7)+(dataBus>>1))   
				elif (OpCode == 8    ):  ALU_imOut = dataBus+OperandReg                   
				elif (OpCode == 9    ):  ALU_imOut = OperandReg-dataBus                   
				elif (OpCode == 10   ):  ALU_imOut = dataBus+OperandReg+Cin           
				elif (OpCode == 11   ):  ALU_imOut = OperandReg-dataBus-Cin           
				elif (OpCode == 12   ):  ALU_imOut = dataBus&OperandReg                  
				elif (OpCode == 13   ):  ALU_imOut = dataBus|OperandReg                  
				elif (OpCode == 14   ):  ALU_imOut = dataBus^OperandReg                  
				elif (OpCode == 15   ):  ALU_imOut = ~(dataBus^OperandReg) & 0xFF
			AluOut.value = ALU_imOut%256
			#Flag Register Update #consoder making the flag pipe a queue
			FlagRegister = [(ALU_imOut/256),~(ALU_imOut/256),(ALUout.value == 0),~(ALUout.value == 0),~(ALUout.value&(1<<7)),(~ALUout.value&(1<<7)),(parityof(ALUout.value)),~(parityof(ALUout.value))]
		Barrier1.wait()
		# Synchronous Here after
		# no regs and synchronous activity in the ALU module ?
		Barrier2.wait()
		if(Kill == 1 ): return
	return

def StackPointerModule(ControlBits,DataBus,StackPointer,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	StackPointer.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		DSP = ControlBits[8] #cached for Synchronous Protection
		ISP = ControlBits[9] #cached for Synchronous Protection
		if(ControlBits[4] == '1'):
			DataBus.put(ProgramCounter.value)
		Barrier1.wait()
		# Synchronous Here after
		if( DSP == '1' and ISP == '0'):
			StackPointer.value = StackPointer.value - 1 # .value requirement ? Not Required :)
		if( ISP == '1' and DSP == '0'):
			StackPointer.value = StackPointer.value + 1  # .value requirement ? Not Required :)
		if( ISP == '1' and DSP == '1'):
			StackPointer.value = DataBus.get()
		Barrier2.wait()
		if(Kill == 1 ): return
	return
	
def FlagRegisterModule(ControlBits,AluFlag,RegSel,SelectedFlag,Kill,Barrier1,Barrier2):
	# reads pipe in on SAL and modifys the flag register
	#init this register to 0101010101
	# read save SAL
	# if SAL then Read from queue and assign to registers
	# output FL into The CCG read Queue id EFL in encountered
	# Loopity Loop :P
	return

def InstructionRegisterModule(ControlBits,DataBus,InstructionRegister,Kill,Barrier1,Barrier2):
	#initialisation
	InstructionRegister.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LIR = ControlBits[10] #cached for Synchronous Protection
		if(LIR == '1'):
			InstructionRegister.value  = DataBus.get()
		Barrier1.wait()
		#use this opportunity to set RegSel Value
		# Synchronous Here after
		Barrier2.wait()
		if(Kill == 1 ): return
	return

def RegisterArrayModule(ControlBits,DataBus,RegisterArray,RegSel,AluOut,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	RegisterArray = [0,1,2,3,4,5,6,7]
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LR0 = ControlBits[18] #cached for Synchronous Protection
		LRN = ControlBits[20] #cached for Synchronous Protection
		SAL = ControlBits[17] #cached for Synchronous Protection
		REGSEL = RegSel.value
		if(ControlBits[19] == '1'):
			DataBus.put(RegisterArray[0])
		if(ControlBits[21] == '1'):
			DataBus.put(RegisterArray[REGSEL])
		Barrier1.wait()
		# Synchronous Here after
		if( LR0 == '1' and SAL == '0'):
			RegisterArray = [0,0,0,0,0,0,0,0]
			a = AluOut.get() # a useless pop to clear the queue
		elif( LR0 == '1' and SAL == '0'):
			RegisterArray[0] = DataBus.get() # .value requirement ? Not Required :)
		elif( LRN == '1' and SAL == '0'):
			RegisterArray[REGSEL] = DataBus.get()  # .value requirement ? Not Required :)
		elif( LR0 == '1' and SAL == '1'):
			RegisterArray[0] = AluOut.get()  # .value requirement ? Not Required :)
		elif( LRN == '1' and SAL == '1'):
			RegisterArray[REGSEL] = AluOut.get()  # .value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill == 1 ): return
	return

def ControlCodeGenerator(ControlBits,InstructionRegister,SelectedFlag,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	counter=0
	CCGConfFile = open('machCode.bin')
	while(counter<256):
		line = MEMConfFile.readline()
		Memory[counter] = (int(line,2)) # control bit arr append and read subsequent
		counter = counter+1	
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		WR = ControlBits[1] #cached for Synchronous Protection
		if(ControlBits[2]== '1'): address = ProgramCounter.value
		elif(ControlBits[3]== '1'): address = StackPointer.value
		else: address = RegisterArray[0] 
		if(ControlBits[0] == '1'):
			DataBus.put(Memory[address])
		Barrier1.wait()
		# Synchronous Here after
		if( WR == '1'):
			Memory[address] = DataBus.get() #value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill.value == 1 ): return
	return
	
	#opens control Code generator csv aand line by line reads the machine states
	#it then moves through the state machien and issues control codes on the 
	#  0, 1 ,2  , 3  , 4  , 5  , 6  , 7  , 8  , 9  , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 
	# RD,WR,S_PC,S_SP,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,E_FL,S_IF,E_IP,L_OP,E_OR,L_OR,S_AL,L_R0,E_R0,L_RN,E_RN



#Shared Variables & Datapaths
DataBus = Queue()
AluOut = Value(c_ubyte, 0, lock=False) # make this a queue and put values spl case of no SAL for ClC case


AluOut = Value(c_ubyte, 0, lock=False)
AluOpcode = Value(c_ubyte, 0, lock=False)
CarryIn = Value(c_ubyte, 0, lock=False)
ProgramCounter = Value(c_ubyte, 0, lock=False)
InstructionRegister = Value(c_ubyte, 0, lock=False)
OperandRegister = Value(c_ubyte, 0, lock=False)
StackPointer = Value(c_ubyte, 0, lock=False)
Kill = Value(c_ubyte, 0, lock=False)
RegSel = Value(c_ubyte, 0, lock=False)#needs Cacheing


IO_In = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
IO_Out = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
Memory = Array(c_ubyte, 256, lock=False)
FlagRegister = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
RegisterArray = Array(c_ubyte,[1,2,3,4,5,6,7,8] , lock=False)
ControlBits = Array(c_char,b'Hello', lock=False ) # needs to be Cached


Barrier1 = Barrier(5)
Barrier2 = Barrier(5)



ThrRegArr = Process(target=RegisterArrayModule, args=(ControlBits,DataBus,RegisterArray,RegSel,AluOut,Kill,Barrier1,Barrier2))
ControlCodeGenerator(ControlBits,InstructionRegister,SelectedFlag,Kill,Barrier1,Barrier2):




print(RegisterArray[1])
print(RegisterArray[3])
print(RegisterArray[5])
print(RegisterArray[7])

P1.start()




P1.join()


print(RegisterArray[1])
print(RegisterArray[3])
print(RegisterArray[5])
print(RegisterArray[7])
print("No issue in init :D")
