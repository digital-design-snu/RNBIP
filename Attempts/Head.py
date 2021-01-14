##------------------------------------------------------------------------------ 
#                     			  The RNBIP
#							Visualisation Encoder
#                     This Multi threaded module 1:1 emulates
# 					 The operation of the RNBIP Micro-Controller
#						Author :: @CommandPaul ( Paul George )
#							   Sophomore Year 2016
#							  Shiv Nadar University
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

import threading
import time

# 	Initialising & Instantiating inter module Signals
posedgeClk=0
S_SP	= 0
S_PC	= 0
RD		= 0
WR		= 0
E_PC	= 0
I_PC	= 0
L_PC	= 0
E_SP	= 0
D_SP	= 0
I_SP	= 0
L_IR	= 0
S_AL	= 0
L_R0	= 0
L_RN	= 0
E_R0	= 0
E_RN	= 0
E_OR	= 0
L_OR	= 0
E_IP	= 0
L_OP	= 0
E_FL	= 0
S_IF	= 0

dataBus	= 0
PC_reg = 0
OperandReg = 0
SP_Address = 255

OR_ALU	= 0
SP_AS	= 0
PC_AS	= 0
R0_AS	= 0
ALU_RN	= 0
opcode	= 0
OR_PC	= 0
ALU_FR	= 0
ALU_FR_Carry	= 0
FR_CG	= 0
Address_Bus	= 0
E_FLi	= 0
S_IFi	= 0
PCOut	= 0
MEMOut	= 0
OROut	= 0
SPOut	= 0
RAOut	= 0
IOOut	= 0
ioOut0	= 0

#this segment of code reads the Memory configuration file into the Mem Array 
counter=0
blockMem= []
MEMConfFile = open('machCode.bin')
while(counter<256):
	line = MEMConfFile.readline()
	blockMem.append(int(line,2))
	counter = counter+1
#Segment Ends
#this Segment of code Sets up the Register Array
counter=0
Reg_Array= []
while(counter<8):
	Reg_Array.append(counter)
	counter = counter+1
#Segment Ends

#move the code below into a While 1 loop for continually driven signals

E_FLi = E_FL;
S_IFi = S_IF;
led2 = PC_AS;
led1 = ioOut0;
SP_Address = (SP_Address-1) if D_SP else SP_Address;
MEMout = blockMem[Address_Bus]

# 	Instantiating Functional blocks of the Architecture 
def BusArbt():
	while(1):
		if(RD): dataBus	= MEMOut
		elif(E_PC): dataBus = PCOut  
		elif(E_SP): dataBus = SPOut  
		elif(E_IP): dataBus = IOOut 
		elif(E_OR): dataBus = OROut 
		elif( E_R0 | E_RN): dataBus	= RAout
		else: dataBus = 0

#Memory Module
def Mem():
	while(1):
		while(posedgeClk):
			if(WR):	blockMem[Address_Bus] = dataBus
			#add some gate delay ?
			

def Alu():
	while(1):
		i = i+1
#Alu

#Address Selector
def AddressSel():
	while(1):
		i=i-1

#Program Counter
def ProgramCounter():
	while(1):
		while(posedgeClk):
			if  (I_PC == 0 and L_PC == 0) :  PC_reg = PC_reg
			elif(I_PC == 1 and L_PC == 0) :  PC_reg = PC_reg + 1
			elif(I_PC == 0 and L_PC == 1) :  PC_reg = dataBus
			else:PC_reg = OperandReg


def InstReg():
	while(1):
		i=i-1
#Instruction Register

def OperandRegister():
	while(1):
		i=i-1
#Operand Register

#Control Code Generator
# this has a bug take updated from Abhimanyu / Prasanna :P and make the edit

#block that updates the state bit
def ControlCodeGeneratorT1():
	while(1):
		while(posedgeClk):
			if(GoFetch):
				State = 0
			else:
				State = 1

#####
#this module updates continually driven signals		
def ControlCodeGeneratorT2():
	while(1):
		while(posedgeClk):
			i=i+1
#####

#Register Array
def RegisterAr():
	while(1):
		while(posedgeClk):
			if(L_R0 and L_RN):
				Reg_Array[0]= 0; 
				Reg_Array[1]= 0; 
				Reg_Array[2]= 0; 
				Reg_Array[3]= 0; 
				Reg_Array[4]= 0; 
				Reg_Array[5]= 0; 
				Reg_Array[6]= 0; 
				Reg_Array[7]= 0;  
			elif(L_R0): Reg_Array[0] =  ALU_out if (S_AL) else dataBus
			elif(L_RN):	Reg_Array[RN_Reg_Sel] = ALU_out if (S_AL) else dataBus_in;

def FlagArray():
	global killthr
	while(killthr):
		print(blockMem[i])
	return
#Flag Array

#Stack Pointer
def StackPointer():
	global killthr
	while(killthr):
		while(posedgeClk):
			if  (I_SP == 0 and D_SP == 0) :  SP_Address = SP_Address
			elif(I_SP == 1 and D_SP == 0) :  SP_Address = SP_Address + 1
			elif(I_SP == 0 and D_SP == 1) :  SP_Address = SP_Address - 1
			else:SP_Address = dataBus
	return

#Control Code Generator
def CtSigDrv():
	global i
	global killthr
	while(killthr):
		i = (i+1)%10
		print("This Is Thread 1 ")
		time.sleep(0.0000001)
	return

#The Top Clock Module and Output File printing module
def TopModule():
	global posedgeClk
	while(1):
	#issue posedge
		posedgeClk = 1
	#delay
	#kill posedge
		posedgeClk = 0
	#delay more
	#write state into vis driver file
	#loop
i = 0
killthr = 1 # a negative logic flag 
print("This Executes till Here :)")
ThrCtrlCodeGen = threading.Thread(target=CtSigDrv)
ThrFlagReg = threading.Thread(target=FlagArray)

ThrCtrlCodeGen.start()
ThrFlagReg.start()
while(notReady)
killthr = 0
ThrCtrlCodeGen.join()
ThrFlagReg.join()

#start threads here

# Start top Module 

# Finish Up :)



	

