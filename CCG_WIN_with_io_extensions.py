##-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# The RNBIP Emulator
# This Multi threaded module 1: 1 emulates the operation of the RNBIP Micro - Controller
# Author::@CommandPaul(Paul George)# Junior Year 2016 - 17
# Shiv Nadar University 
##-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

##-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#   This Python Script is hierarchially seperated into the original modulles of
#   the architecture, all original signals have been preserved the encoded data
#   can be visualised in VedantCJ(Vedant Chakravarty `s) Visualisation module
#   Developed in C++ using the QT Framework , The input to this file should be
#   in the format output by the Pn337(Prasanna Natarajan) Assembler .
##-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#---- Fixit Comments Remove from final
# Re-Write this in cpp
#---- End of Fixit Comments

#   Note :: The killthr flag is negative logic

#   Import Libraries
import time
from multiprocessing import Process,Value,Queue,Array,Barrier
from ctypes import c_ubyte,c_char,c_int
import ctypes
import multiprocessing, logging
import random
import pdb
import os
import datetime;
import platform
import re
import sys
import tkinter as tk
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
	for k in range(0,8):
		RegisterArray[k] = random.randint(0,255)
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
		# print(RegisterArray)

		Barrier2.wait()
		if(Kill.value == 1 ):
			#           print("Bye - Reg Arr")
			return
	return

## Additions for Prof. Biswas`s Requested Realtime IO Request Feature

class IO_Interface(tk.Tk):
	def __init__(self,IO_In,IO_Out):
		tk.Tk.__init__(self)
		#self.C_IO_In = IO_In
		#self.C_IO_Out = IO_Out
		self.title('Virtual IO Interface')
		self.data = None
		self.entries = []
		for i in range(1,12):
			if i == 1:
				row = tk.Frame(self) 
				lab1 = tk.Label(row, width=8,text= "Port",anchor='center',borderwidth=2, relief="groove")
				lab2 = tk.Label(row, width=25,text="Output",anchor='center',borderwidth=2, relief="groove")
				lab3 = tk.Label(row, width=75,text="Input[current value]",anchor='center',borderwidth=2, relief="groove")
				row.pack( fill=tk.X, padx=5, pady=5)
				lab1.pack(side=tk.LEFT,fill=tk.X)
				lab2.pack(side=tk.LEFT,fill=tk.X,expand=tk.YES)
				lab3.pack(side=tk.LEFT,fill=tk.X,expand=tk.YES)
				#ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
				#self.entries.append(ent)
			elif(i==2):
				row = tk.Frame(self) 
				row.pack( fill=tk.X, padx=5, pady=5)
				lab1 = tk.Label(row, width=5,text="",anchor='center',justify = 'center',borderwidth=2, relief="flat")
				lab1.pack(side=tk.LEFT,expand=tk.YES)
				lab2 = tk.Label(row, width=5,text="HEX",anchor='center',justify = 'center',borderwidth=2, relief="raised")
				lab2.pack(side=tk.LEFT,expand=tk.YES)
				for j in range (7,-1,-1) :
					lab = tk.Label(row, width=1,text=str(j),anchor='center',justify = 'center')
					lab.pack(side=tk.LEFT,fill=tk.X,expand=tk.YES)
				lab = tk.Label(row, width=2,text="")
				lab.pack(side=tk.LEFT,expand=tk.YES)
				lab3 = tk.Label(row, width=6,text="HEX",anchor='center',justify = 'center',borderwidth=2, relief="raised")
				lab3.pack(side=tk.LEFT,expand=tk.YES)
				lab = tk.Label(row, width=1,text="")
				lab.pack(side=tk.LEFT,expand=tk.YES)
				for j in range (7,-1,-1) :
					lab = tk.Label(row, width=1,text="")
					lab.pack(side=tk.LEFT,expand=tk.YES)
					lab = tk.Label(row, width=3,text=str(j),anchor='center',justify = 'center')
					lab.pack(side=tk.LEFT,fill=tk.X,expand=tk.YES)
			elif(i==11):
				row = tk.Frame(self)
				row.pack( fill=tk.X, padx=5, pady=5,expand=tk.YES)
				self.update_Button = tk.Button(row, width=40, text='Commit Changes(if any) & Continue',command=lambda:self.update_io(IO_In,IO_Out)) 
				self.update_Button.pack(side=tk.BOTTOM,expand=tk.YES)
			else:
				row = tk.Frame(self) 
				row.pack( fill=tk.X, padx=5, pady=5,expand=tk.YES)
				lab1 = tk.Label(row, width=5,text=str(i-3),anchor='center',justify = 'center',borderwidth=2, relief="flat")
				lab1.pack(side=tk.LEFT,expand=tk.YES)
				lab2 = tk.Label(row, width=5,text=str(IO_Out[i-3]),anchor='center',justify = 'center',borderwidth=2, relief="raised")
				lab2.pack(side=tk.LEFT,expand=tk.YES)
				for j in range (7,-1,-1) :
					lab = tk.Label(row, width=1,text=str((IO_Out[i-3]&(1<<j))>>j),anchor='w')
					lab.pack(side=tk.LEFT,fill=tk.X,expand=tk.YES)
				lab = tk.Label(row, width=2,text="")
				lab.pack(side=tk.LEFT,expand=tk.YES)
				ent = tk.Entry(row,width = 7,justify = 'center',borderwidth=2, relief="raised")
				ent.insert(5,str(IO_In[i-3]))
				ent.pack(side=tk.LEFT, fill=tk.X,expand=tk.YES)
				ent8v = []
				for j in range (7,-1,-1) :
					lab = tk.Label(row, width=2,text="")
					lab.pack(side=tk.LEFT,expand=tk.YES)
					EntB = tk.Entry(row, width=3,justify = 'center')
					EntB.insert(3,str((IO_In[i-3]&(1<<j))>>j))
					EntB.pack(side=tk.LEFT,fill=tk.X,expand=tk.YES)				
					ent8v.append(EntB)
				self.entries.append((ent,ent8v))
		#self.update_Button.pack(row,expand=tk.YES, fill=tk.X)
		#self.update_Button.grid(row=1, column=1, padx=8, pady=8)
		
	def update_io(self,IO_In,IO_Out):
		for i in range(0,8):
			k = 0
			for j in range (0,8):	
				# Reconstruct the Byte Here
				inp = int(self.entries[i][1][j].get())
				if(inp != 0 )and(inp != 1):
					print("Error in input")
					return -1
				k = inp +2*k;
			hexk = int(self.entries[i][0].get())
			if(hexk!=k and hexk == IO_In[i]):
				IO_In[i]=k
			elif(hexk!=k and k == IO_In[i]):
				IO_In[i] = hexk
			#IO_In[i] = self.entries[i]
		self.destroy()

	#IO_Interface_Update(IO_In,IO_Out,master)
## End of Additions - CommandPaul
def IOModule(ControlBits,InstructionRegister,IO_In,IO_Out,DataBus,Kill,Barrier1,Barrier2):
	#initialisation
	IO_In  = [1,3,5,7,9,11,13,15]
	IO_Out = [2,4,6,8,10,12,14,16]
	Barrier2.wait()
	#Setup Main Loop
	while(1):
		LOP = ControlBits[14] #cached for Synchronous Protection
		REGSEL = InstructionRegister.value%8 #cached for Synchronous Protection
		if(ControlBits[13] == b'1'):
			# Tkinter Code Here
			print("Hey")
			interface = IO_Interface(IO_In,IO_Out)
			interface.mainloop()
			print("Yo")
			print(IO_In)
			DataBus.put(IO_In[REGSEL])
		Barrier1.wait()
		# Synchronous Here after
		if( LOP == b'1'):
			IO_Out[REGSEL] = DataBus.get() # .value requirement ? Not Required :)
			interface = IO_Interface(IO_In,IO_Out)
			interface.mainloop()
			print(IO_Out)
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
				elif (OpCode == 6    ):  ALU_imOut = ((dataBus<<1)+CarryIn)
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
	MEMConfFile = open('memory.bin')
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
			while(counter<256): # Persist Memory state at the end of the smulation This needs the correct operation of the step function
				outFile = open("memory.bin","w")
				output = bin(Memory[counter])[2:].zfill(8)
				outFile.write(output+"\n");
				counter = counter+1
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
			# print("Bye - pc")
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
			#print("bye - ir")
			#print(counter)
			return
	return
def log(x):
	flag=0;
	#print(datetime.datetime.now());
	if len(str(x)) ==1:
		x = '0'+str(x);
	if len(str(x)) == 2:
			if str(x)[0] in ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','0'] and str(x)[1] in ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','0'] :
				return x;
				return x;
	return(str(datetime.datetime.now())+" "+"Error @ "+" \""+str(x)+"\" is not a recognised command\n")

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
		#   print(ControlBits[i],end=" ")
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
	#print("storeValuesToOutputFile called\n")
	#print("ControlBits are \t" , end=" ")
	#for i in range(0, 22):
		#print("",int(ControlBits[i],2), end=' ')
	for i in range(0, 22):
		if i != 0:
			f.write(" ")
		f.write(str(int(ControlBits[i], 2)))
	f.write(" ")
	#print("State = ", end=' ')
	#print(State.value)
	f.write(str(int(State.value)))
	f.write(" ")
	#print("\nProgramCounter = ", end=' ')
	#print(hex(ProgramCounter.value))
	f.write(str(ProgramCounter.value))
	f.write(" ")
	#print("\nStackPointer = ", end=' ')
	#print(hex(StackPointer.value))
	f.write(str(StackPointer.value))
	f.write(" ")
	#print("\nOperandRegister = ", end=' ')
	#print(hex(OperandRegister.value))
	f.write(str(OperandRegister.value))
	f.write(" ")
	#print("\nInstructionRegister = ", end=' ')
	#print(hex(InstructionRegister.value))
	f.write(str(InstructionRegister.value))
	f.write(" ")
	#print("\nFlagArray = ", end=' ')
	#for i in range(0, 8):
		#print(FlagArray[i], end=' ')
	for i in range(0, 8):
		f.write(" ")
		f.write(str(FlagArray[i]))
	#print("\nRegisterArray = ", end=' ')
	#for i in range(0, 8):
		#print(hex(RegisterArray[i]), end=' ')
	for i in range(0, 8):
		f.write(" ")
		f.write(str(RegisterArray[i]))
	#print("\nMemory = ", end=' ')
	#for i in range(0, 256):
		#print(hex(Memory[i]), end=' ')
	for i in range(0, 256):
		f.write(" ")
		f.write(str(Memory[i]))
	f.write('\n')
	# print(Memory, end=' ')
	f.close()
def fname(x):
	return{
		'NOP': 'NOP',
		"CLR": "CLR",
		"CLC": "CLC",
		"JUD": "JUD",
		"JUA": "JUA",
		"NOT R0": "NOT R0",
		"NOT R1": "NOT R1",
		"NOT R2": "NOT R2",
		"NOT R3": "NOT R3",
		"NOT R4": "NOT R4",
		"NOT R5": "NOT R5",
		"NOT R6": "NOT R6",
		"NOT R7": "NOT R7",
		"JUA": "JUA",
		"CUD": "CUD",
		"CUA": "CUA",
		"RTU": "RTU",
		"LSP": "LSP",
		"MVD": "MVD",
		"RSP": "RSP",
		"MVS": "MVS",
		"RLA": "RLA",
		"RRA": "RRA",
		"JCD Z": "JCD R0",
		"JCD NZ": "JCD R1",
		"JCD C": "JCD R2",
		"JCD NC": "JCD R3",
		"JCD P": "JCD R4",
		"JCD N": "JCD R5",
		"JCD OP": "JCD R6",
		"JCD EP": "JCD R7",
		"MVD R0": "MVD R0",
		"MVD R1": "MVD R1",
		"MVD R2": "MVD R2",
		"MVD R3": "MVD R3",
		"MVD R4": "MVD R4",
		"MVD R5": "MVD R5",
		"MVD R6": "MVD R6",
		"MVD R7": "MVD R7",
		"MVS R0": "MVS R0",
		"MVS R1": "MVS R1",
		"MVS R2": "MVS R2",
		"MVS R3": "MVS R3",
		"MVS R4": "MVS R4",
		"MVS R5": "MVS R5",
		"MVS R6": "MVS R6",
		"MVS R7": "MVS R7",
		"JCA Z": "JCA R0",
		"JCA NZ": "JCA R1",
		"JCA C": "JCA R2",
		"JCA NC": "JCA R3",
		"JCA P": "JCA R4",
		"JCA N": "JCA R5",
		"JCA OP": "JCA R6",
		"JCA EP": "JCA R7",
		"CCD Z": "CCD R0",
		"CCD NZ": "CCD R1",
		"CCD C": "CCD R2",
		"CCD NC": "CCD R3",
		"CCD P": "CCD R4",
		"CCD N": "CCD R5",
		"CCD OP": "CCD R6",
		"CCD EP": "CCD R7",
		"CCA Z": "CCA R0",
		"CCA NZ": "CCA R1",
		"CCA C": "CCA R2",
		"CCA NC": "CCA R3",
		"CCA P": "CCA R4",
		"CCA N": "CCA R5",
		"CCA OP": "CCA R6",
		"CCA EP": "CCA R7",
		"INC R0": "INC R0",
		"INC R1": "INC R1",
		"INC R2": "INC R2",
		"INC R3": "INC R3",
		"INC R4": "INC R4",
		"INC R5": "INC R5",
		"INC R6": "INC R6",
		"INC R7": "INC R7",
		"RTC Z": "RTC R0",
		"RTC NZ": "RTC R1",
		"RTC C": "RTC R2",
		"RTC NC": "RTC R3",
		"RTC P": "RTC R4",
		"RTC N": "RTC R5",
		"RTC OP": "RTC R6",
		"RTC EP": "RTC R7",
		"DCR R0": "DCR R0",
		"DCR R1": "DCR R1",
		"DCR R2": "DCR R2",
		"DCR R3": "DCR R3",
		"DCR R4": "DCR R4",
		"DCR R5": "DCR R5",
		"DCR R6": "DCR R6",
		"DCR R7": "DCR R7",
		"MVI R0": "MVI R0",
		"MVI R1": "MVI R1",
		"MVI R2": "MVI R2",
		"MVI R3": "MVI R3",
		"MVI R4": "MVI R4",
		"MVI R5": "MVI R5",
		"MVI R6": "MVI R6",
		"MVI R7": "MVI R7",
		"STA R0": "STA R0",
		"STA R1": "STA R1",
		"STA R2": "STA R2",
		"STA R3": "STA R3",
		"STA R4": "STA R4",
		"STA R5": "STA R5",
		"STA R6": "STA R6",
		"STA R7": "STA R7",
		"PSH R0": "PSH R0",
		"PSH R1": "PSH R1",
		"PSH R2": "PSH R2",
		"PSH R3": "PSH R3",
		"PSH R4": "PSH R4",
		"PSH R5": "PSH R5",
		"PSH R6": "PSH R6",
		"PSH R7": "PSH R7",
		"LDA R0": "LDA R0",
		"LDA R1": "LDA R1",
		"LDA R2": "LDA R2",
		"LDA R3": "LDA R3",
		"LDA R4": "LDA R4",
		"LDA R5": "LDA R5",
		"LDA R6": "LDA R6",
		"LDA R7": "LDA R7",
		"POP R0": "POP R0",
		"POP R1": "POP R1",
		"POP R2": "POP R2",
		"POP R3": "POP R3",
		"POP R4": "POP R4",
		"POP R5": "POP R5",
		"POP R6": "POP R6",
		"POP R7": "POP R7",
		"ADA R0": "ADA R0",
		"ADA R1": "ADA R1",
		"ADA R2": "ADA R2",
		"ADA R3": "ADA R3",
		"ADA R4": "ADA R4",
		"ADA R5": "ADA R5",
		"ADA R6": "ADA R6",
		"ADA R7": "ADA R7",
		"ADI R0": "ADI R0",
		"ADI R1": "ADI R1",
		"ADI R2": "ADI R2",
		"ADI R3": "ADI R3",
		"ADI R4": "ADI R4",
		"ADI R5": "ADI R5",
		"ADI R6": "ADI R6",
		"ADI R7": "ADI R7",
		"SBA R0": "SBA R0",
		"SBA R1": "SBA R1",
		"SBA R2": "SBA R2",
		"SBA R3": "SBA R3",
		"SBA R4": "SBA R4",
		"SBA R5": "SBA R5",
		"SBA R6": "SBA R6",
		"SBA R7": "SBA R7",
		"SBI R0": "SBI R0",
		"SBI R1": "SBI R1",
		"SBI R2": "SBI R2",
		"SBI R3": "SBI R3",
		"SBI R4": "SBI R4",
		"SBI R5": "SBI R5",
		"SBI R6": "SBI R6",
		"SBI R7": "SBI R7",
		"ACA R0": "ACA R0",
		"ACA R1": "ACA R1",
		"ACA R2": "ACA R2",
		"ACA R3": "ACA R3",
		"ACA R4": "ACA R4",
		"ACA R5": "ACA R5",
		"ACA R6": "ACA R6",
		"ACA R7": "ACA R7",
		"ACI R0": "ACI R0",
		"ACI R1": "ACI R1",
		"ACI R2": "ACI R2",
		"ACI R3": "ACI R3",
		"ACI R4": "ACI R4",
		"ACI R5": "ACI R5",
		"ACI R6": "ACI R6",
		"ACI R7": "ACI R7",
		"SCA R0": "SCA R0",
		"SCA R1": "SCA R1",
		"SCA R2": "SCA R2",
		"SCA R3": "SCA R3",
		"SCA R4": "SCA R4",
		"SCA R5": "SCA R5",
		"SCA R6": "SCA R6",
		"SCA R7": "SCA R7",
		"SCI R0": "SCI R0",
		"SCI R1": "SCI R1",
		"SCI R2": "SCI R2",
		"SCI R3": "SCI R3",
		"SCI R4": "SCI R4",
		"SCI R5": "SCI R5",
		"SCI R6": "SCI R6",
		"SCI R7": "SCI R7",
		"ANA R0": "ANA R0",
		"ANA R1": "ANA R1",
		"ANA R2": "ANA R2",
		"ANA R3": "ANA R3",
		"ANA R4": "ANA R4",
		"ANA R5": "ANA R5",
		"ANA R6": "ANA R6",
		"ANA R7": "ANA R7",
		"ANI R0": "ANI R0",
		"ANI R1": "ANI R1",
		"ANI R2": "ANI R2",
		"ANI R3": "ANI R3",
		"ANI R4": "ANI R4",
		"ANI R5": "ANI R5",
		"ANI R6": "ANI R6",
		"ANI R7": "ANI R7",
		"ORA R0": "ORA R0",
		"ORA R1": "ORA R1",
		"ORA R2": "ORA R2",
		"ORA R3": "ORA R3",
		"ORA R4": "ORA R4",
		"ORA R5": "ORA R5",
		"ORA R6": "ORA R6",
		"ORA R7": "ORA R7",
		"ORI R0": "ORI R0",
		"ORI R1": "ORI R1",
		"ORI R2": "ORI R2",
		"ORI R3": "ORI R3",
		"ORI R4": "ORI R4",
		"ORI R5": "ORI R5",
		"ORI R6": "ORI R6",
		"ORI R7": "ORI R7",
		"XRA R0": "XRA R0",
		"XRA R1": "XRA R1",
		"XRA R2": "XRA R2",
		"XRA R3": "XRA R3",
		"XRA R4": "XRA R4",
		"XRA R5": "XRA R5",
		"XRA R6": "XRA R6",
		"XRA R7": "XRA R7",
		"XRI R0": "XRI R0",
		"XRI R1": "XRI R1",
		"XRI R2": "XRI R2",
		"XRI R3": "XRI R3",
		"XRI R4": "XRI R4",
		"XRI R5": "XRI R5",
		"XRI R6": "XRI R6",
		"XRI R7": "XRI R7",
		"INA P0": "INA R0",
		"INA P1": "INA R1",
		"INA P2": "INA R2",
		"INA P3": "INA R3",
		"INA P4": "INA R4",
		"INA P5": "INA R5",
		"INA P6": "INA R6",
		"INA P7": "INA R7",
		"OUT P0": "OUT R0",
		"OUT P1": "OUT R1",
		"OUT P2": "OUT R2",
		"OUT P3": "OUT R3",
		"OUT P4": "OUT R4",
		"OUT P5": "OUT R5",
		"OUT P6": "OUT R6",
		"OUT P7": "OUT R7",
	}.get(x,log(x));
def f(x):
	return{

	   "NOP":  '00000000',
	   "CLR":  '00000001',
	   "CLC":  '00000010',
	   "JUD":  '00000011',
	   "JUA":  '00000100',
	   "NOT R0":    '00100000',
	   "NOT R1":    '00100001',
	   "NOT R2":    '00100010',
	   "NOT R3":    '00100011',
	   "NOT R4":    '00100100',
	   "NOT R5":    '00100101',
	   "NOT R6":    '00100110',
	   "NOT R7":    '00100111',
	   "JUA":    '00000100',
	   "CUD":    '00000101',
	   "CUA":    '00000110',
	   "RTU":    '00000111',
	   "LSP":    '00010000',
	   "RSP":    '00011000',
	   "RLA":    '01100000',
	   "RRA":    '01110000',
	   "JCD R0":    '00001000',
	   "JCD R1":    '00001001',
	   "JCD R2":    '00001010',
	   "JCD R3":    '00001011',
	   "JCD R4":    '00001100',
	   "JCD R5":    '00001101',
	   "JCD R6":    '00001110',
	   "JCD R7":    '00001111',
	   "MVD R0":    '00010000',
	   "MVD R1":    '00010001',
	   "MVD R2":    '00010010',
	   "MVD R3":    '00010011',
	   "MVD R4":    '00010100',
	   "MVD R5":    '00010101',
	   "MVD R6":    '00010110',
	   "MVD R7":    '00010111',
	   "MVS R0":    '00011000',
	   "MVS R1":    '00011001',
	   "MVS R2":    '00011010',
	   "MVS R3":    '00011011',
	   "MVS R4":    '00011100',
	   "MVS R5":    '00011101',
	   "MVS R6":    '00011110',
	   "MVS R7":    '00011111',
	   "JCA R0":    '00101000',
	   "JCA R1":    '00101001',
	   "JCA R2":    '00101010',
	   "JCA R3":    '00101011',
	   "JCA R4":    '00101100',
	   "JCA R5":    '00101101',
	   "JCA R6":    '00101110',
	   "JCA R7":    '00101111',
	   "CCD R0":    '00110000',
	   "CCD R1":    '00110001',
	   "CCD R2":    '00110010',
	   "CCD R3":    '00110011',
	   "CCD R4":    '00110100',
	   "CCD R5":    '00110101',
	   "CCD R6":    '00110110',
	   "CCD R7":    '00110111',
	   "CCA R0":    '00111000',
	   "CCA R1":    '00111001',
	   "CCA R2":    '00111010',
	   "CCA R3":    '00111011',
	   "CCA R4":    '00111100',
	   "CCA R5":    '00111101',
	   "CCA R6":    '00111110',
	   "CCA R7":    '00111111',
	   "INC R0":    '01000000',
	   "INC R1":    '01000001',
	   "INC R2":    '01000010',
	   "INC R3":    '01000011',
	   "INC R4":    '01000100',
	   "INC R5":    '01000101',
	   "INC R6":    '01000110',
	   "INC R7":    '01000111',
	   "RTC R0":    '01001000',
	   "RTC R1":    '01001001',
	   "RTC R2":    '01001010',
	   "RTC R3":    '01001011',
	   "RTC R4":    '01001100',
	   "RTC R5":    '01001101',
	   "RTC R6":    '01001110',
	   "RTC R7":    '01001111',
	   "DCR R0":    '01010000',
	   "DCR R1":    '01010001',
	   "DCR R2":    '01010010',
	   "DCR R3":    '01010011',
	   "DCR R4":    '01010100',
	   "DCR R5":    '01010101',
	   "DCR R6":    '01010110',
	   "DCR R7":    '01010111',
	   "MVI R0":    '01011000',
	   "MVI R1":    '01011001',
	   "MVI R2":    '01011010',
	   "MVI R3":    '01011011',
	   "MVI R4":    '01011100',
	   "MVI R5":    '01011101',
	   "MVI R6":    '01011110',
	   "MVI R7":    '01011111',
	   "STA R0":    '01100000',
	   "STA R1":    '01100001',
	   "STA R2":    '01100010',
	   "STA R3":    '01100011',
	   "STA R4":    '01100100',
	   "STA R5":    '01100101',
	   "STA R6":    '01100110',
	   "STA R7":    '01100111',
	   "PSH R0":    '01101000',
	   "PSH R1":    '01101001',
	   "PSH R2":    '01101010',
	   "PSH R3":    '01101011',
	   "PSH R4":    '01101100',
	   "PSH R5":    '01101101',
	   "PSH R6":    '01101110',
	   "PSH R7":    '01101111',
	   "LDA R0":    '01110000',
	   "LDA R1":    '01110001',
	   "LDA R2":    '01110010',
	   "LDA R3":    '01110011',
	   "LDA R4":    '01110100',
	   "LDA R5":    '01110101',
	   "LDA R6":    '01110110',
	   "LDA R7":    '01110111',
	   "POP R0":    '01111000',
	   "POP R1":    '01111001',
	   "POP R2":    '01111010',
	   "POP R3":    '01111011',
	   "POP R4":    '01111100',
	   "POP R5":    '01111101',
	   "POP R6":    '01111110',
	   "POP R7":    '01111111',
	   "ADA R0":    '10000000',
	   "ADA R1":    '10000001',
	   "ADA R2":    '10000010',
	   "ADA R3":    '10000011',
	   "ADA R4":    '10000100',
	   "ADA R5":    '10000101',
	   "ADA R6":    '10000110',
	   "ADA R7":    '10000111',
	   "ADI R0":    '10001000',
	   "ADI R1":    '10001001',
	   "ADI R2":    '10001010',
	   "ADI R3":    '10001011',
	   "ADI R4":    '10001100',
	   "ADI R5":    '10001101',
	   "ADI R6":    '10001110',
	   "ADI R7":    '10001111',
	   "SBA R0":    '10010000',
	   "SBA R1":    '10010001',
	   "SBA R2":    '10010010',
	   "SBA R3":    '10010011',
	   "SBA R4":    '10010100',
	   "SBA R5":    '10010101',
	   "SBA R6":    '10010110',
	   "SBA R7":    '10010111',
	   "SBI R0":    '10011000',
	   "SBI R1":    '10011001',
	   "SBI R2":    '10011010',
	   "SBI R3":    '10011011',
	   "SBI R4":    '10011100',
	   "SBI R5":    '10011101',
	   "SBI R6":    '10011110',
	   "SBI R7":    '10011111',
	   "ACA R0":    '10100000',
	   "ACA R1":    '10100001',
	   "ACA R2":    '10100010',
	   "ACA R3":    '10100011',
	   "ACA R4":    '10100100',
	   "ACA R5":    '10100101',
	   "ACA R6":    '10100110',
	   "ACA R7":    '10100111',
	   "ACI R0":    '10101000',
	   "ACI R1":    '10101001',
	   "ACI R2":    '10101010',
	   "ACI R3":    '10101011',
	   "ACI R4":    '10101100',
	   "ACI R5":    '10101101',
	   "ACI R6":    '10101110',
	   "ACI R7":    '10101111',
	   "SCA R0":    '10110000',
	   "SCA R1":    '10110001',
	   "SCA R2":    '10110010',
	   "SCA R3":    '10110011',
	   "SCA R4":    '10110100',
	   "SCA R5":    '10110101',
	   "SCA R6":    '10110110',
	   "SCA R7":    '10110111',
	   "SCI R0":    '10111000',
	   "SCI R1":    '10111001',
	   "SCI R2":    '10111010',
	   "SCI R3":    '10111011',
	   "SCI R4":    '10111100',
	   "SCI R5":    '10111101',
	   "SCI R6":    '10111110',
	   "SCI R7":    '10111111',
	   "ANA R0":    '11000000',
	   "ANA R1":    '11000001',
	   "ANA R2":    '11000010',
	   "ANA R3":    '11000011',
	   "ANA R4":    '11000100',
	   "ANA R5":    '11000101',
	   "ANA R6":    '11000110',
	   "ANA R7":    '11000111',
	   "ANI R0":    '11001000',
	   "ANI R1":    '11001001',
	   "ANI R2":    '11001010',
	   "ANI R3":    '11001011',
	   "ANI R4":    '11001100',
	   "ANI R5":    '11001101',
	   "ANI R6":    '11001110',
	   "ANI R7":    '11001111',
	   "ORA R0":    '11010000',
	   "ORA R1":    '11010001',
	   "ORA R2":    '11010010',
	   "ORA R3":    '11010011',
	   "ORA R4":    '11010100',
	   "ORA R5":    '11010101',
	   "ORA R6":    '11010110',
	   "ORA R7":    '11010111',
	   "ORI R0":    '11011000',
	   "ORI R1":    '11011001',
	   "ORI R2":    '11011010',
	   "ORI R3":    '11011011',
	   "ORI R4":    '11011100',
	   "ORI R5":    '11011101',
	   "ORI R6":    '11011110',
	   "ORI R7":    '11011111',
	   "XRA R0":    '11100000',
	   "XRA R1":    '11100001',
	   "XRA R2":    '11100010',
	   "XRA R3":    '11100011',
	   "XRA R4":    '11100100',
	   "XRA R5":    '11100101',
	   "XRA R6":    '11100110',
	   "XRA R7":    '11100111',
	   "XRI R0":    '11101000',
	   "XRI R1":    '11101001',
	   "XRI R2":    '11101010',
	   "XRI R3":    '11101011',
	   "XRI R4":    '11101100',
	   "XRI R5":    '11101101',
	   "XRI R6":    '11101110',
	   "XRI R7":    '11101111',
	   "INA P0":    '11110000',
	   "INA P1":    '11110001',
	   "INA P2":    '11110010',
	   "INA P3":    '11110011',
	   "INA P4":    '11110100',
	   "INA P5":    '11110101',
	   "INA P6":    '11110110',
	   "INA P7":    '11110111',
	   "OUT P0":    '11111000',
	   "OUT P1":    '11111001',
	   "OUT P2":    '11111010',
	   "OUT P3":    '11111011',
	   "OUT P4":    '11111100',
	   "OUT P5":    '11111101',
	   "OUT P6":    '11111110',
	   "OUT P7":    '11111111',

	}.get(x,x)

def f1(x):
	return{
		"0":    '0000',
		"1":    '0001',
		"2":    '0010',
		"3":    '0011',
		"4":    '0100',
		"5":    '0101',
		"6":    '0110',
		"7":    '0111',
		"8":    '1000',
		"9":    '1001',
		"A":    '1010',
		"B":    '1011',
		"C":    '1100',
		"D":    '1101',
		"E":    '1110',
		"F":    '1111',
	}[x]


def file_len(fname):
	i=0;
	with fname as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def tobin(x):
	binary = '';
	if len(x) == 2:
		for i in x:
			# print(i)
			binary = binary+f1(i.strip());
	elif len(x)==1:
		x="0"+x;
		for i in x:
			binary = binary+f1(i.strip());
	return binary;

def Check_Signal():
	UI_Signals = open(os.path.dirname(os.path.abspath('__file__'))+"\\sig.dat")
	line = UI_Signals.readline()
	UI_Signals.close()
	while(line=="0\n"):
		UI_Signals = open(os.path.dirname(os.path.abspath('__file__'))+"\\sig.dat")
		line = UI_Signals.readline()
		if((line!="0\n" ) and (line!="1\n") and (line!="2\n")):
			line="0\n"
		UI_Signals.close()
		#print("Here 0")
	if(line=="1\n"):
		#print("Here 1")
		return 1;
	while(line=="2\n"):
		return 10;
		UI_Signals = open(os.path.dirname(os.path.abspath('__file__'))+"\\sig.dat")
		line = UI_Signals.readline()
		if((line!="0\n" ) and (line!="1\n") and (line!="2\n")):
			line="2\n"
		#print("Here 2")
		UI_Signals.close()
	#print("Step")
	return 1;

def main():
	#print("OLA AMIGOS")

	list_of_od_operations=["MVI R","ADI R","SBI R","ACI R","SCI R","ANI R","ORI R","XRI R","JUD","CUD","JCD R","CCD R","JCA R","CCA R","RTC R"]
	for codes in list_of_od_operations:
		if "R" == codes[len(codes)-1]:
			for i in range(0,8):
				list_of_od_operations.append(codes+str(i))
	list_of_flags = ["Z","NZ","C","NC","P","N","OP","EP"]
	if platform.system() == "Windows":
		inpFile = open(os.path.dirname(os.path.abspath('__file__'))+"\\user_input.txt")
		#"C:\\Users\\prasanna\\Desktop\\user_input.txt");
		outFile = open(os.path.dirname(os.path.abspath('__file__'))+"\\input.txt","w");
		logFile = open(os.path.dirname(os.path.abspath('__file__'))+"\\log.txt","w");
		tempFile = open(os.path.dirname(os.path.abspath('__file__'))+"\\temp.txt","w");
		#print(os.path.dirname(__file__))
		counter = 0;
		flag=1;
		labels = [];

		for line in inpFile:
			if "//" in line.strip():
				if "/" in line[0].strip():
					continue;
				else:
					line = line[0:line.index('//')];
					##print("outside else JUD")
					if "JUD" in line:
						##print("inside else JUD")
						t = line[[m.start() for m in re.finditer(r" ",line)][0]:]
						line = " JUD "+t
						##print("this is it"+ line.strip())
					if "CUD" in line:
						t = line[[m.start() for m in re.finditer(r" ",line)][0]:]
						line = " CUD "+t
					if " " in line.strip():
						if len([m.start() for m in re.finditer(r" ",line)]) > 1:

							temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
							if temp.strip() in list_of_flags:
								temp = "0"+str(list_of_flags.index(temp.strip()))
							line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
							line = fname(line.strip())
							if line.strip() in list_of_od_operations:
								line = line + "\n" + temp
							else:
								print("inside first else")
								line = log(line)+ "\n" + temp

				output = line.strip();
				print(output);
				if len(output) < 20:
					tempFile.write(output+"\n");
				else:
					print("inside log")
					logFile.write('Error at ' + output)
					sys.exit()
			elif line[0]=="":
				continue;
			else:
				##print("outside else JUD")
				if "JUD " in line:
					##print("inside else JUD")
					t = line[[m.start() for m in re.finditer(r" ",line)][0]:]
					line = " JUD "+t
					##print("this is it"+ line.strip())
				if "CUD " in line:
						t = line[[m.start() for m in re.finditer(r" ",line)][0]:]
						line = " CUD "+t
				if " " in line.strip():
					if len([m.start() for m in re.finditer(r" ",line)]) > 1:
						#print("inside if")
						temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
						if temp.strip() in list_of_flags:
							temp = "0"+str(list_of_flags.index(temp.strip()))
						line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
						line = fname(line.strip())
						if line.strip() in list_of_od_operations:
							#print("inside od list")
							#print (line)
							line = line + "\n" + temp
						else:
							print("inside log else")
							line = log(line)+ "\n" + temp

			if len(line) < 20:
				#print(line)
				tempFile.write(line);
			else:
				print("here")
				logFile.write('Error at ' + line);
				sys.exit()

		tempFile.close();
		print("done")
		tempFile = open(os.path.dirname(os.path.abspath('__file__'))+"\\temp.txt")
		for line in tempFile:
			counter = counter+1;
			lab=0;
			if line[0]=="\n":
				continue
			if ":" in line.strip():
				labels.append((counter,line[0:line.index(':')]));
				# print(labels);
				if len(labels)!=0:
						for x in labels:
							if x[1] == line[line.index(':')+1:].strip():
								# print(x[0])
								output = fname(x[0]);
								# print(output);
								outFile.write(str(output)+"\n");
								break


				if line[line.index(':')+1] == "\n":
					continue
				else:
					is_inside = 0
					line = line[line.index(':')+1:].strip()
					if " " in line.strip():
						if len([m.start() for m in re.finditer(r" ",line)]) > 1:
							is_inside=1
							temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
							if temp.strip() in list_of_flags:
								temp = "0"+str(list_of_flags.index(temp.strip()))
							line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
							line = fname(line)
							if line.strip() in list_of_od_operations:
								line = line.upper() + "\n" + temp
							else:
								line = log(line.upper())+ "\n" + temp
							# line = line.upper() + "\n" + temp

					output = line.strip()

					# output = line[line.index(':')+1:].strip().upper();
					print(output);
					if is_inside == 1:
						if len(output)<20:
							outFile.write(output+"\n");
						else:
							sys.exit()
							logFile.write('Error at ' + output);
					else:
						output = fname(line.strip().upper())
						if len(output)<20:
							outFile.write(output+"\n")
						else:
							sys.exit()
							logFile.write('Error at ' + output);
			else:
				if len(labels)!=0:
						for x in labels:
							if x[1] == line.strip():
								# print(x[0])
								output = fname(x[0]);
								# print(output);
								outFile.write(str(output)+"\n");
								lab=1;
								break
				if lab==0:
					is_inside = 0;
					if " " in line.strip():
						if len([m.start() for m in re.finditer(r" ",line)]) > 1:
							print("if")
							print(line)
							is_inside = 1;
							temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
							if temp.strip() in list_of_flags:
								temp = "0"+str(list_of_flags.index(temp.strip()))
							line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
							line = fname(line)
							if line.strip() in list_of_od_operations:
								print("here od")
								line = line.upper() + "\n" + temp
							else:
								print("not od")
								line = log(line.upper())+ "\n" + temp

					output = line.strip();
					#print(output);
					#print("hherererererer")
					if is_inside == 1:
						if len(output)<20:
							outFile.write(output+"\n");
						else:
							print("logFile")
							logFile.write('Error at ' + output);
							sys.exit()
					else:
						#print("this is where it should be:"+line)
						tempx = 0
						output = f(line.strip().upper())
						print(output)
						if output.isdigit():
							tempx=1
						try:
							int(output, 16)
							tempx = 1
						except ValueError:
							tempx = 0
						if len(output)<20 and tempx==1 :
							outFile.write(output+"\n")
						else:
							print("lof 2")
							logFile.write('Error at ' + output);
							sys.exit()

		if flag == 1:
			#print(str(datetime.datetime.now()));
			logFile.write(str(datetime.datetime.now())+" Compilation Successful...\n");



	else:
		inpFile = open(os.path.dirname(__file__)+"user_input.txt")
		#"C:\\Users\\prasanna\\Desktop\\user_input.txt");
		outFile = open(os.path.dirname(__file__)+"input.txt","w");
		logFile = open(os.path.dirname(__file__)+"log.txt","w");
		tempFile = open(os.path.dirname(__file__)+"temp.txt","w");
		#print(os.path.dirname(__file__))
		counter = 0;
		flag=1;
		labels = [];
		for line in inpFile:
			if "//" in line.strip():
				if "/" in line[0].strip():
					continue;
				else:
					line = line[0:line.index('//')];
					if " " in line.strip():
						if len([m.start() for m in re.finditer(r" ",line)]) > 1:
							temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
							if temp.strip() in list_of_flags:
								temp = "0"+str(list_of_flags.index(temp.strip()))
							line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
							line = fname(line.strip())
							if line.strip() in list_of_od_operations:
								line = line + "\n" + temp
							else:
								line = log(line.strip())+ "\n" + temp

					output = line.strip();
					print("This "+output);

					if len(output) <20:
						tempFile.write(line);
					else:
						logFile.write('Error at ' + line);

			elif line[0]=="":
				continue;
			else:
				if " " in line.strip():
					if len([m.start() for m in re.finditer(r" ",line)]) > 1:

						temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
						if temp.strip() in list_of_flags:
							temp = "0"+str(list_of_flags.index(temp.strip()))
						line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
						line = fname(line.strip())
						if line.strip() in list_of_od_operations:
							line = line + "\n" + temp
						else:
							line = log(line)+ "\n" + temp
				output = line.strip()
				if len(output) <20:

					tempFile.write(line);
				else:
					logFile.write('Error at ' + line);

		tempFile.close();
		tempFile = open(os.path.dirname(__file__)+"temp.txt")
		for line in tempFile:
			counter = counter+1;
			lab=0;
			if line[0]=="\n":
				continue
			if ":" in line.strip():
				labels.append((counter,line[0:line.index(':')]));
				# print(labels);
				if len(labels)!=0:
						for x in labels:
							if x[1] == line[line.index(':')+1:].strip():
								# print(x[0])
								if len(x[0])==1:
									output = fname('0'+x[0]);
								else:
									output = fname(x[0]);

								# print(output);
								outFile.write(str(output)+"\n");
								break


				if line[line.index(':')+1] == "\n":
					continue
				else:
					line = line[line.index(':')+1:].strip()
					if " " in line.strip():
						if len([m.start() for m in re.finditer(r" ",line)]) > 1:

							temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
							if temp.strip() in list_of_flags:
								temp = "0"+str(list_of_flags.index(temp.strip()))
							line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
							line = fname(line)
							if line.strip() in list_of_od_operations:
								line = line.upper() + "\n" + temp
							else:
								line = log(line.upper())+ "\n" + temp
							# line = line.upper() + "\n" + temp

					output = line.strip()

					print(output);
					if len(output)<20:
						outFile.write(output+"\n");
					else:
						logFile.write('Error at ' + output);

			else:
				if len(labels)!=0:
						for x in labels:
							if x[1] == line.strip():
								# print(x[0])

								if len(x[0])==1:
									output = fname('0'+x[0]);
								else:
									output = fname(x[0]);

								# print(output);
								outFile.write(str(output)+"\n");
								lab=1;
								break
				if lab==0:
					if len(line)<20:
						if " " in line.strip():
							if len([m.start() for m in re.finditer(r" ",line)]) > 1:
								temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
								if temp.strip() in list_of_flags:
									temp = "0"+str(list_of_flags.index(temp.strip()))
								line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
								line = fname(line)
								if line.strip() in list_of_od_operations:
									line = line.upper() + "\n" + temp
								else:
									line = log(line.upper())+ "\n" + temp
								# line = line.upper() + "\n" + temp

						output = line.strip()
						outFile.write(output+"\n");
					else:
						logFile.write('Error at ' + output);

		if flag == 1:
			#print(str(datetime.datetime.now()));
			logFile.write(str(datetime.datetime.now())+" End...\n");


		# print(platform.system())
	logFile.close()

	inpFile = open("input.txt");
	outFile = open("memory.bin","w")
	#ControlFile = open("cc.txt","w")
	for line in inpFile:
		if "//" not in line.strip():
			output = f(line.strip());
			# print(output);
			if output.strip() != "":
				try:
					int(output.strip(),16)
					if len(output) <= 2:
						output = bin(int(output.strip(),16))[2:].zfill(8)

					#print "this is the output: "+output
				except ValueError:
					output = output.strip()

				outFile.write(output+"\n");

	outFile.close();
	#os.path.dirname(__file__)+
	read_out_File = open("memory.bin","r");
	num_lines = file_len(read_out_File)
	# print(num_lines);
	read_out_Fil = open("memory.bin","r");
	'''for line in read_out_Fil:
		# print(line.strip())
		cc = toCB(line.strip());
		# print(cc)
		ControlFile.write(toCB(line.strip()));'''

	read_out_File.close();
	#ControlFile.close();
	appendFile = open("memory.bin","a");
	# Add feature to read persistance on and then open old state file and read last memory segment
	while num_lines<=255:
		appendFile.write("00000000"+"\n");
		num_lines+=1;
	appendFile.close();

	inpFile.close();
	outFile.close();

	Ncyc = 20
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
	#RegSel = Value(c_ubyte, 0, lock=False)#needs Cacheing
	State = Value(c_ubyte, 0, lock=False)

	IO_In = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
	IO_Out = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
	Memory = Array(c_ubyte, 256, lock=False)
	FlagRegister = Array(c_ubyte,[1,0,0,1,1,0,0,1] , lock=False)
	RegisterArray = Array(c_ubyte,[1,2,3,4,5,6,7,8] , lock=False)
	ControlBits = Array(c_char,b'1010010000100000000000', lock=False ) # needs to be Cached


	Barrier1 = Barrier(10) # dont forget ot update :P
	Barrier2 = Barrier(10)

	open('output', 'w').close()

	#Thread Instantiation
	ThrCCG = Process(target=ControlCodeGenerator,args=(ControlBits,IR_CCG,FlagRegister,State,Kill,Barrier1,Barrier2))
	ThrIR = Process(target=InstructionRegister_Module,args=(ControlBits,InstructionRegister,DataBus,IR_CCG,Kill,Barrier1,Barrier2))
	ThrPC = Process(target=ProgramCounterModule,args=(ControlBits,ProgramCounter,OperandRegister,DataBus,Kill,Barrier1,Barrier2))
	ThrMEM = Process(target=MemoryModule,args=(ControlBits,ProgramCounter,RegisterArray,StackPointer,DataBus,Memory,Kill,Barrier1,Barrier2))
	ThrRegArr = Process(target=RegisterArrayModule,args=(ControlBits,DataBus,RegisterArray,InstructionRegister,AluOut,Kill,Barrier1,Barrier2))
	ThrALU = Process(target=ALU_Module,args=(ControlBits,DataBus,OperandRegister,InstructionRegister,CarryIn,AluOut,FlagRegister,Kill,Barrier1,Barrier2))
	ThrSPtr = Process(target=StackPointerModule,args =(ControlBits,DataBus,StackPointer,ProgramCounter,Kill,Barrier1,Barrier2))
	ThrOpReg = Process(target=OperandRegisterModule,args=(ControlBits,OperandRegister,DataBus,Kill,Barrier1,Barrier2))
	ThrIO = Process(target=IOModule,args=(ControlBits,InstructionRegister,IO_In,IO_Out,DataBus,Kill,Barrier1,Barrier2)) ## EDIT Regsel was not wired to the I0 Module

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
		if(N==1):
			N = Check_Signal()
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
	#print("No issue in init :D")

if __name__ == '__main__':
	#mpl = multiprocessing.log_to_stderr()
	#mpl.setLevel(logging.DEBUG)
	main()