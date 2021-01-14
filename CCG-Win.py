##------------------------------------------------------------------------------ 
#                     			  The RNBIP
#							Visualisation Encoder
#								aka. Voyager2
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
#3 :: stack pointer module needs a program counter iniitialisation
#---- End of Fixit Comments

#	the killthr flag is negative logic 

#	Import Libraries

import time
from multiprocessing import Process,Value,Queue,Array,Barrier
from ctypes import c_ubyte,c_char,c_int
import ctypes
import multiprocessing, logging
import pdb

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
'''
def Test_Module(ControlBits,InstructionRegister,SelectedFlag,Kill,Barrier1,Barrier2):
	Barrier2.wait()
	while(1):
		Barrier1.wait()
		Barrier2.wait()
	return
'''
def parityOf(number):
	parity = 0
	int_type = number
	while (int_type > 0):
		parity = ~parity
		int_type = int_type & (int_type - 1)
	return(parity + 1)

def RegisterArrayModule(ControlBits,DataBus,RegisterArr,InstructionRegister,AluOut,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	RegisterArray = [0,1,2,3,4,5,6,7]
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LR0 = ControlBits[18] #cached for Synchronous Protection
		LRN = ControlBits[20] #cached for Synchronous Protection
		SAL = ControlBits[17] #cached for Synchronous Protection
		REGSEL = InstructionRegister.value %8
		#print(LR0,LRN,SAL,REGSEL)
		
		if(ControlBits[19] == b'1'):
			DataBus.put(RegisterArray[0])
		
		if(ControlBits[21] == b'1'):
			DataBus.put(RegisterArray[REGSEL])
		
		Barrier1.wait()
		# Synchronous Here after
		if( LR0 == b'1' and LRN == b'1'):
			RegisterArray = [0,0,0,0,0,0,0,0]
			#a = AluOut.get() # a useless pop to clear the queue
		elif( LR0 == b'1' and SAL == b'0'):
			RegisterArray[0] = DataBus.get() # .value requirement ? Not Required :)
		elif( LRN == b'1' and SAL == b'0'):
			RegisterArray[REGSEL] = DataBus.get()  # .value requirement ? Not Required :)
		elif( LR0 == b'1' and SAL == b'1'):
			RegisterArray[0] = AluOut.value  # .value requirement ? Not Required :)
		elif( LRN == b'1' and SAL == b'1'):
			RegisterArray[REGSEL] = AluOut.value  # .value requirement ? Not Required :)
		for k in range(0,8):
			RegisterArr[k] = RegisterArray[k]
		print(RegisterArray)
		
		Barrier2.wait()
		if(Kill.value == 1 ): 
			print("Bye - Reg Arr")
			return
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
		if(ControlBits[13] == b'1'):
			DataBus.put(IO_In[RegSel.value])
		Barrier1.wait()
		# Synchronous Here after
		if( LOP == b'1'):
			IO_Out[REGSEL] = DataBus.get() # .value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill.value == 1 ): return
	return

	
def OperandRegisterModule(ControlBits,OperandRegister,DataBus,Kill,Barrier1,Barrier2):
	#initialisation
	OperandRegister.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LOR = ControlBits[16] #cached for Synchronous Protection
		if(ControlBits[15] == b'1'):
			DataBus.put(OperandRegister.value)
		Barrier1.wait()
		# Synchronous Here after
		if( LOR == b'1'):
			OperandRegister.value = DataBus.get() # .value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill.value == 1 ): return
	return

def ALU_Module(ControlBits,DataBus,OperandRegister,InstructionRegister,CarryIn,AluOut,FlagRegister,Kill,Barrier1,Barrier2):
	#initialisation
	OperandRegister.value = 0
	ALU_imOut = c_int(0) 
	FR = [1,0,0,1,1,0,0,1]
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		SAL = ControlBits[17] #cached for Synchronous Protection
		OpCode = InstructionRegister.value >> 4 #for faster Switch below :|
		#print(OpCode)
		if(SAL == b'1'):
			if   (OpCode == 0    ):  ALU_imOut = 0                            
			else :
				dataBus = DataBus.get()
				OperandReg = OperandRegister.value
				CarryIn = FR[2]
				if   (OpCode == 1    ):  ALU_imOut = dataBus                
				elif (OpCode == 2    ):  ALU_imOut = (~dataBus & 0x1FF) # the 1FF is maintainance of a design descision          
				elif (OpCode == 3    ):  ALU_imOut = OperandReg                          
				elif (OpCode == 4    ):  ALU_imOut = dataBus+1                  
				elif (OpCode == 5    ):  ALU_imOut = dataBus-1                  
				elif (OpCode == 6    ):  ALU_imOut = (dataBus<<1+CarryIn)           
				elif (OpCode == 7    ):  ALU_imOut = (((dataBus%2)<<8)+(CarryIn<<7)+(dataBus>>1))   
				elif (OpCode == 8    ):  ALU_imOut = dataBus+OperandReg                   
				elif (OpCode == 9    ):  ALU_imOut = OperandReg-dataBus                   
				elif (OpCode == 10   ):  ALU_imOut = dataBus+OperandReg+CarryIn
				elif (OpCode == 11   ):  ALU_imOut = OperandReg-dataBus-CarryIn
				elif (OpCode == 12   ):  ALU_imOut = dataBus&OperandReg                  
				elif (OpCode == 13   ):  ALU_imOut = dataBus|OperandReg                  
				elif (OpCode == 14   ):  ALU_imOut = dataBus^OperandReg                  
				elif (OpCode == 15   ):  ALU_imOut = ~(dataBus^OperandReg) & 0x1FF # the 1FF is maintainance of a design descision          
			AluOut.value = ALU_imOut%256
			ALU_imOut = ALU_imOut%512
			
			#print(AluOut.value)
			#Flag Register Update #consoder making the flag pipe a queue			
			#ALU_imOut = int(ALU_imOut)
			FR = [(ALU_imOut%256 == 0),(ALU_imOut%256 != 0),(ALU_imOut >= 256),not (ALU_imOut >= 256),((((ALU_imOut%256)&(1<<7))>>7)==0),(((~(ALU_imOut%256)&(1<<7))>>7)==0),(parityOf(ALU_imOut%256)==0),(parityOf(ALU_imOut%256)==1)]
			for k in range(0,8):
				FlagRegister[k] = FR[k]
			#print("FLags")
			#print(FlagRegister[4],end = " ")
			#print(FlagRegister[5])
			#print("ALU OUT  == = == ",end = " ")
			#print(FR,end = " ")
			#print(ALU_imOut)
			#print([chr(ALU_imOut / 256), ~chr(ALU_imOut / 256), (ALU_imOut == 0), ~(ALU_imOut == 0),~(ALU_imOut & (1 << 7)), (~ALU_imOut & (1 << 7)), (parityof(ALU_imOut)),~(parityof(ALU_imOut))])
		Barrier1.wait()
		# Synchronous Here after
		# no regs and synchronous activity in the ALU module ?
		Barrier2.wait()
		if(Kill.value == 1 ): return
	return

def StackPointerModule(ControlBits,DataBus,StackPointer,ProgramCounter,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	StackPointer.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		DSP = ControlBits[8] #cached for Synchronous Protection
		ISP = ControlBits[9] #cached for Synchronous Protection
		# i deleted ESP when removing EPC
		if(ControlBits[7] == b'1'):
			DataBus.put(StackPointer.value)
		Barrier1.wait()
		# Synchronous Here after
		if( DSP == b'1' and ISP == b'0'):
			StackPointer.value = (StackPointer.value - 1)%256 # .value requirement ? Not Required :)
		if( ISP == b'1' and DSP == b'0'):
			StackPointer.value = (StackPointer.value + 1)%256  # .value requirement ? Not Required :)
		if( ISP == b'1' and DSP == b'1'):
			StackPointer.value = DataBus.get()
		Barrier2.wait()
		if(Kill.value == 1 ): return
	return


def MemoryModule(ControlBits,ProgramCounter,RegisterArray,StackPointer,DataBus,Memory,Kill,Barrier1,Barrier2):	
	#initialisation read from file			
	counter=0
	MEMConfFile = open('stress1.bin')
	while(counter<256):
		line = MEMConfFile.readline()
		Memory[counter] = (int(line,2))
		counter = counter+1	
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		DSP = ControlBits[8]
		WR = ControlBits[1] #cached for Synchronous Protection
		if(ControlBits[2]== b'1'): address = ProgramCounter.value
		elif(ControlBits[3]== b'1'): address =  StackPointer.value if (DSP == b'0') else (StackPointer.value - 1)%256 
		else: address = RegisterArray[0] 
		if(ControlBits[0] == b'1'):
			DataBus.put(Memory[address])
		Barrier1.wait()
		# Synchronous Here after
		if( WR == b'1'):
			Memory[address] = DataBus.get() #value requirement ? Not Required :)
		Barrier2.wait()
		if(Kill.value == 1 ):
			print("Bye - mem")
			return
	return

def ProgramCounterModule(ControlBits,ProgramCounter,OperandRegister,DataBus,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	ProgramCounter.value = 0
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LPC = ControlBits[6] #cached for Synchronous Protection
		IPC = ControlBits[5] #cached for Synchronous Protection
		if(ControlBits[4] == b'1'):
			DataBus.put(ProgramCounter.value)
		Barrier1.wait()
		# Synchronous Here after
		if (  LPC == b'1' and IPC == b'0'):
			#pdb.set_trace()
			#print(DataBus.get())
			ProgramCounter.value = DataBus.get() # .value requirement ? Not Required :)
			#print(ProgramCounter.value)
		elif( LPC == b'0' and IPC == b'1'):
			ProgramCounter.value = (ProgramCounter.value + 1)%256  # .value requirement ? Not Required :)
		elif( LPC == b'1' and IPC == b'1'):
			ProgramCounter.value = OperandRegister.value  # .value requirement ? Not Required :)
		Barrier2.wait()
		#print("ProgramCounter ",end=" ")
		#print(ProgramCounter.value)
		if(Kill.value == 1 ):
			print("Bye - pc")
			return
	return

def InstructionRegister_Module(ControlBits,InstructionRegister,DataBus,IR_CCG,Kill,Barrier1,Barrier2):
	InstructionRegister.value = 0
	counter = 0 # Diagnostic For runtime counting
	Barrier2.wait()
	while(1):
		L_IR = ControlBits[10] #cached for Synchronous Protection
		Barrier1.wait()
		if(L_IR == b'1' ) : 
			InstructionRegister.value = DataBus.get()
			IR_CCG.put(InstructionRegister.value)
		Barrier2.wait()
		counter = counter +1
		if(Kill.value == 1 ):
			print("bye - ir")
			print(counter) 
			return
	return

def ControlCodeGenerator(ControlBits,IR_CCG,FlagRegister,State,Kill,Barrier1,Barrier2):
	#initialisation read from file			
	
	counter=0
	IR = 0
	CCG_LUT = []
	FL = False
	CCGConfFile = open('machCode.bin')
	while(counter<512):
		line = CCGConfFile.readline()
		Temp_Pointer = ctypes.create_string_buffer(line.encode())
		CCG_LUT.append(Temp_Pointer) #(int(line,2)) # control bit arr append and read subsequent # Computationally less expensive eats memory :P
		counter = counter+1	
	

	#looks good :)
	State.value = 0
	ctypes.memmove(ControlBits,ctypes.create_string_buffer(b'1010010000100000000000'), 23) # Essentially Initialise for fetch
	print("CCG Init Complete")
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		#print("0  , 1 , 2  , 3  , 4  , 5  , 6  , 7  , 8  , 9  , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 ")
		#print("RD , WR ,S_PC,S_SP,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,E_FL,S_IF,E_IP,L_OP,E_OR,L_OR,S_AL,L_R0,E_R0,L_RN,E_RN")
		#for i in range(0,22):
		#	print(ControlBits[i],end=" ")
		#print(".")
		# cache existing control bbits and start acting on the same
		L_IR = ControlBits[10] #cached for synchronousnous Protection
		E_FL = ControlBits[11] #cached for Synchronous Protection
		S_IF = ControlBits[12] #cached for Synchronous Protection
		#Selected Flag :P
		#Fetch Logic (FL + E FL ) * S IF = 1. Selected FLAg  ?
		#print(S_IF)
		if (E_FL == b'1')  : FL =  FlagRegister[IR%8]
		
		FETCH = ((S_IF == b'1') and ((not (E_FL == b'1') or not(FL == True ))))
		Barrier1.wait()
		# if fetch condition detected then wait on the queue to read form IR   Reset State and push th bits for fetch
		# else issue
		if( FETCH == 1 ): 
			#print("Fetch")
			State.value = 0
			ctypes.memmove(ControlBits,ctypes.create_string_buffer(b'1010010000100000000000'), 23)# eqv of checking the CCG LUT for Space 0 :P
		else:
			#print("No_Fetch")
			if (L_IR == b'1'):
				IR = IR_CCG.get()
			ctypes.memmove(ControlBits,CCG_LUT[IR*2 +State.value], 23)
			State.value = (State.value + 1) %2
		
		Barrier2.wait()
		if(Kill.value == 1 ): 
			print("Bye - ccg")
			return
	return	
	#opens control Code generator csv aand line by line reads the machine states
	#it then moves through the state machien and issues control codes on the 
	#  0, 1 ,2  , 3  , 4  , 5  , 6  , 7  , 8  , 9  , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 
	# RD,WR,S_PC,S_SP,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,E_FL,S_IF,E_IP,L_OP,E_OR,L_OR,S+_AL,L_R0,E_R0,L_RN,E_RN

def storeValuesToOutputFile(ControlBits,State,ProgramCounter,StackPointer,OperandRegister,InstructionRegister,FlagArray,RegisterArray,Memory):
    f = open('output','a')
    print("storeValuesToOutputFile called\n")
    print("ControlBits are \t" , end=" ")
    for i in range(0, 22):
        print("",int(ControlBits[i],2), end=' ')
    for i in range(0, 22):
        if i != 0:
            f.write(" ")
        f.write(str(int(ControlBits[i], 2)))
    f.write(" ")
    print("State = ", end=' ')
    print(State.value)
    f.write(str(int(State.value))) 
    f.write(" ")
    print("\nProgramCounter = ", end=' ')
    print(hex(ProgramCounter.value))
    f.write(str(ProgramCounter.value))
    f.write(" ")
    print("\nStackPointer = ", end=' ')
    print(hex(StackPointer.value))
    f.write(str(StackPointer.value))
    f.write(" ")
    print("\nOperandRegister = ", end=' ')
    print(hex(OperandRegister.value))
    f.write(str(OperandRegister.value))
    f.write(" ")
    print("\nInstructionRegister = ", end=' ')
    print(hex(InstructionRegister.value))
    f.write(str(InstructionRegister.value))
    f.write(" ")
    print("\nFlagArray = ", end=' ')
    for i in range(0, 8):
        print(FlagArray[i], end=' ')
    for i in range(0, 8):
        f.write(" ")
        f.write(str(FlagArray[i]))
    print("\nRegisterArray = ", end=' ')
    for i in range(0, 8):
        print(hex(RegisterArray[i]), end=' ')
    for i in range(0, 8):
        f.write(" ")
        f.write(str(RegisterArray[i]))
    print("\nMemory = ", end=' ')
    for i in range(0, 256):
        print(hex(Memory[i]), end=' ')
    for i in range(0, 256):
        f.write(" ")
        f.write(str(Memory[i]))
    f.write('\n')
    # print(Memory, end=' ')
    f.close()

def main():
	print("OLA AMIGOS")
	Ncyc = int(input())
	#Shared Variables & Datapaths
	DataBus = Queue()
	IR_CCG = Queue()
	#SelectedFlag = Queue()
	AluOut = Value(c_ubyte, 0, lock=False) # make this a queue and put values spl case of no SAL for ClC case


	#AluOut = Value(c_ubyte, 0, lock=False)
	AluOpcode = Value(c_ubyte, 0, lock=False)
	CarryIn = Value(c_ubyte, 0, lock=False)
	ProgramCounter = Value(c_ubyte, 0, lock=False)
	InstructionRegister = Value(c_ubyte, 0, lock=False)
	OperandRegister = Value(c_ubyte, 0, lock=False)
	StackPointer = Value(c_ubyte, 0, lock=False)
	Kill = Value(c_ubyte, 0, lock=False)
	RegSel = Value(c_ubyte, 0, lock=False)#needs Cacheing
	State = Value(c_ubyte, 0, lock=False)

	IO_In = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
	IO_Out = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
	Memory = Array(c_ubyte, 256, lock=False)
	FlagRegister = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
	RegisterArray = Array(c_ubyte,[1,2,3,4,5,6,7,8] , lock=False)
	ControlBits = Array(c_char,b'1010010000100000000000', lock=False ) # needs to be Cached


	Barrier1 = Barrier(10) # dont forget ot update :P
	Barrier2 = Barrier(10)

	#Thread Instantiation
	ThrCCG = Process(target=ControlCodeGenerator,args=(ControlBits,IR_CCG,FlagRegister,State,Kill,Barrier1,Barrier2))
	ThrIR = Process(target=InstructionRegister_Module,args=(ControlBits,InstructionRegister,DataBus,IR_CCG,Kill,Barrier1,Barrier2))
	ThrPC = Process(target=ProgramCounterModule,args=(ControlBits,ProgramCounter,OperandRegister,DataBus,Kill,Barrier1,Barrier2))
	ThrMEM = Process(target=MemoryModule,args=(ControlBits,ProgramCounter,RegisterArray,StackPointer,DataBus,Memory,Kill,Barrier1,Barrier2))
	ThrRegArr = Process(target=RegisterArrayModule,args=(ControlBits,DataBus,RegisterArray,InstructionRegister,AluOut,Kill,Barrier1,Barrier2))
	ThrALU = Process(target=ALU_Module,args=(ControlBits,DataBus,OperandRegister,InstructionRegister,CarryIn,AluOut,FlagRegister,Kill,Barrier1,Barrier2))
	ThrSPtr = Process(target=StackPointerModule,args =(ControlBits,DataBus,StackPointer,ProgramCounter,Kill,Barrier1,Barrier2))
	ThrOpReg = Process(target=OperandRegisterModule,args=(ControlBits,OperandRegister,DataBus,Kill,Barrier1,Barrier2))
	ThrIO = Process(target=IOModule,args=(ControlBits,IO_In,IO_Out,DataBus,RegSel,Kill,Barrier1,Barrier2))
	
	#Thread Start
	ThrCCG.start()
	ThrIR.start()
	ThrPC.start()
	ThrMEM.start()
	ThrRegArr.start()
	ThrALU.start()
	ThrSPtr.start()
	ThrOpReg.start()
	ThrIO.start()

	#Issue Kill Signal Here After the satisfaction of somme criterion :P

		#Barrier2.wait()
		#print("After Init")
		#Barrier1.wait()
		#print("After Posedge")
		#thread Monitor and Kill Issue

	#time.sleep(1)
	#this thread jut prints the state of the elements :|
	N = Ncyc
	while(N>0):
		Barrier2.wait()
		storeValuesToOutputFile(ControlBits, State, ProgramCounter, StackPointer, OperandRegister, InstructionRegister,FlagRegister, RegisterArray, Memory)
		Barrier1.wait()
		N = N-1	
	Kill.value  = 1
	Barrier2.wait()
	#Barrier2.wait()
	#print("End Cycle")

	#Join threads and Prepare for Exit
	ThrCCG.join()
	ThrIR.join()
	ThrPC.join()
	ThrMEM.join()
	ThrRegArr.join()
	ThrALU.join()
	ThrSPtr.join()
	ThrOpReg.join()
	ThrIO.join()
	print("No issue in init :D")


if __name__ == '__main__':
	#mpl = multiprocessing.log_to_stderr()
	#mpl.setLevel(logging.DEBUG)
	main()


