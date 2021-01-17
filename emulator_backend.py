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
import datetime
import platform
import re
import sys

from RNBIP_ISA import Architectural_state,Microarchitectural_state
from emulator_io import IO_Interface
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

'''def Proc(StateVariableA,StateVariableB,Kill,Barrier1,Barrier2):
    
    # The design is assumed to be completly synchronous to an implict clock
    # Barriers are used as an analogue to Standard HDL Event Regions, 
    # which help us split the design simulation into independent phases 
    # helping us avoid race conditions on our lock free state variables

    < Initialization Phase >
    StateVariableA.set(0)
    StateVariableB.set(0)

    Barrier2.wait()
    a = StateVariableA.get()+1
    
    while(1):
      StateVariableB.put(a)
      Barrier1.wait()
    
      a = StateVariableA.get()+1
      StateVariableB.put(a)
      Barrier2.wait()
      if(Kill.value == 1 ):
        return
  '''

class single_bus_emulator:

  ## RNBIP Architectural State 
  ProgramCounter = Value(c_ubyte, 0, lock=False)
  StackPointer = Value(c_ubyte, 0, lock=False)
  RegisterArray = Array(c_ubyte,[1,2,3,4,5,6,7,8] , lock=False)
  FlagRegister = Array(c_ubyte,[1,0,0,1,1,0,0,1] , lock=False)
  Memory = Array(c_ubyte, 256, lock=False)
  IO_In = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)
  IO_Out = Array(c_ubyte,[0,0,0,0,0,0,0,0] , lock=False)

  ## RNBIP MicroArchitectural State
  DataBus = Queue()
  IR_CCG = Queue()
  #SelectedFlag = Queue()
  AluOut = Value(c_ubyte, 0, lock=False) # make this a queue and put values spl case of no SAL for ClC case
  #AluOut = Value(c_ubyte, 0, lock=False)
  AluOpcode = Value(c_ubyte, 0, lock=False)
  CarryIn = Value(c_ubyte, 0, lock=False)
  InstructionRegister = Value(c_ubyte, 0, lock=False)
  OperandRegister = Value(c_ubyte, 0, lock=False)
  State = Value(c_ubyte, 0, lock=False)
  ControlBits = Array(c_char,b'1010010000100000000000', lock=False ) # needs to be Cached

  ## Model specific Variables
  Ncyc = 20
  Kill = Value(c_ubyte, 0, lock=False)
  #RegSel = Value(c_ubyte, 0, lock=False)#needs Cacheing
  
  ## Multi Processing and Synchronization State
  ThrCCG = Process()
  ThrIR = Process()
  ThrPC = Process()
  ThrMEM = Process()
  ThrRegArr = Process()
  ThrALU = Process()
  ThrSPtr = Process()
  ThrOpReg = Process()
  ThrIO = Process()
  Barrier1 = Barrier(10) # dont forget ot update :P
  Barrier2 = Barrier(10)

  ## Trace Vector
  TraceVector = []

  ## Housekeeping static members
  @staticmethod
  def parityOf(number):
    parity = 0
    int_type = number
    while (int_type > 0):
      parity = ~parity
      int_type = int_type & (int_type - 1)
    return(parity + 1)

  @staticmethod
  def file_len(fname):
  	i=0;
  	with fname as f:
  		for i, l in enumerate(f):
  			pass
  	return i + 1

  ## State machine static member functions

  @staticmethod
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

  
    #IO_Interface_Update(IO_In,IO_Out,master)
  ## End of Additions - CommandPaul
  @staticmethod
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

  @staticmethod
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

  @staticmethod
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
        FR = [(ALU_imOut%256 == 0),(ALU_imOut%256 != 0),(ALU_imOut >= 256),not (ALU_imOut >= 256),((((ALU_imOut%256)&(1<<7))>>7)==0),(((~(ALU_imOut%256)&(1<<7))>>7)==0),(single_bus_emulator.parityOf(ALU_imOut%256)==0),(single_bus_emulator.parityOf(ALU_imOut%256)==1)]
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
  
  @staticmethod
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

  @staticmethod
  def MemoryModule(ControlBits,ProgramCounter,RegisterArray,StackPointer,DataBus,Memory,Kill,Barrier1,Barrier2):
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
        # while(counter<256): # Persist Memory state at the end of the smulation This needs the correct operation of the step function
        #   outFile = open("memory.bin","w")
        #   output = bin(Memory[counter])[2:].zfill(8)
        #   outFile.write(output+"\n");
        #   counter = counter+1
        return
    return

  @staticmethod
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

  @staticmethod
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

  @staticmethod
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
    # print("CCG Init Complete")
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
        # print("Bye - ccg")
        return
    return
  #opens control Code generator csv aand line by line reads the machine states
  #it then moves through the state machien and issues control codes on the
  #  0, 1 ,2  , 3  , 4  , 5  , 6  , 7  , 8  , 9  , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21
  # RD,WR,S_PC,S_SP,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,E_FL,S_IF,E_IP,L_OP,E_OR,L_OR,S+_AL,L_R0,E_R0,L_RN,E_RN

  def __init__(self):
    counter=0
    while(counter < 256):
      self.Memory[counter] = (int("00000000",2))
      counter = counter+1
    # print("emulator instantiated")

  def load_memory(self,memory_bin):
    counter=0
    self.memory_bin = memory_bin
    for line in self.memory_bin.splitlines():
      self.Memory[counter] = (int(line,2))
      counter = counter+1
    while(counter < 256):
      self.Memory[counter] = (int("00000000",2))
      counter = counter+1

  def start(self):
    #Thread Instantiation
    self.ThrCCG = Process(target=single_bus_emulator.ControlCodeGenerator,args=(self.ControlBits,self.IR_CCG,self.FlagRegister,self.State,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrIR = Process(target=single_bus_emulator.InstructionRegister_Module,args=(self.ControlBits,self.InstructionRegister,self.DataBus,self.IR_CCG,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrPC = Process(target=single_bus_emulator.ProgramCounterModule,args=(self.ControlBits,self.ProgramCounter,self.OperandRegister,self.DataBus,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrMEM = Process(target=single_bus_emulator.MemoryModule,args=(self.ControlBits,self.ProgramCounter,self.RegisterArray,self.StackPointer,self.DataBus,self.Memory,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrRegArr = Process(target=single_bus_emulator.RegisterArrayModule,args=(self.ControlBits,self.DataBus,self.RegisterArray,self.InstructionRegister,self.AluOut,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrALU = Process(target=single_bus_emulator.ALU_Module,args=(self.ControlBits,self.DataBus,self.OperandRegister,self.InstructionRegister,self.CarryIn,self.AluOut,self.FlagRegister,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrSPtr = Process(target=single_bus_emulator.StackPointerModule,args =(self.ControlBits,self.DataBus,self.StackPointer,self.ProgramCounter,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrOpReg = Process(target=single_bus_emulator.OperandRegisterModule,args=(self.ControlBits,self.OperandRegister,self.DataBus,self.Kill,self.Barrier1,self.Barrier2))
    self.ThrIO = Process(target=single_bus_emulator.IOModule,args=(self.ControlBits,self.InstructionRegister,self.IO_In,self.IO_Out,self.DataBus,self.Kill,self.Barrier1,self.Barrier2)) ## EDIT Regsel was not wired to the I0 Module

    #Reset Global State
    self.TraceVector.clear()
    self.Kill.value = 0
    self.ProgramCounter.value = 0
    self.StackPointer.value = 0
    for k in range(0,8):
      self.RegisterArray[k] = random.randint(0,255)
      self.IO_In[k] = 0
      self.IO_Out[k] = 0

    self.FlagRegister[0] = 1
    self.FlagRegister[1] = 0
    self.FlagRegister[2] = 0
    self.FlagRegister[3] = 1
    self.FlagRegister[4] = 1
    self.FlagRegister[5] = 0
    self.FlagRegister[6] = 0
    self.FlagRegister[7] = 1

    ## RNBIP MicroArchitectural State
    self.DataBus = Queue()
    self.IR_CCG = Queue()
    #SelectedFlag = Queue()
    self.AluOut.value = 0
    self.AluOpcode.value = 0
    self.CarryIn.value = 0
    self.InstructionRegister.value = 0
    self.OperandRegister.value = 0
    self.State.value = 0
    ctypes.memmove(self.ControlBits,ctypes.create_string_buffer(b'1010010000100000000000'), 23)


    #Thread Start
    self.ThrCCG.start()
    self.ThrIR.start()
    self.ThrPC.start()
    self.ThrMEM.start()
    self.ThrRegArr.start()
    self.ThrALU.start()
    self.ThrSPtr.start()
    self.ThrOpReg.start()
    self.ThrIO.start()

  def trace_vector_append(self):
    #Arch State
    words = []
    flags = []
    regs  = []
    IO_OUTPUT = []
    IO_INPUT =[]
    for word in self.Memory:
      words.append(word)
    for flag in self.FlagRegister: #ctype unpacking
      flags.append(flag == 1)
    for reg in self.RegisterArray: #ctype unpacking
      regs.append(reg)
    for io_inB in self.IO_In: #ctype unpacking
      IO_INPUT.append(io_inB)
    for io_outB in self.IO_Out: #ctype unpacking
      IO_OUTPUT.append(io_outB)

    arch = Architectural_state(
      PC=self.ProgramCounter.value,
      SP=self.StackPointer.value,
      Registers=regs.copy(),
      Flags=flags.copy(),
      Memory=words.copy(),
      IO_In=IO_INPUT.copy(),
      IO_Out=IO_OUTPUT.copy())
    
    del words, flags, regs , IO_INPUT , IO_OUTPUT
    
    #March State
    control_bits = []
    for cbit in self.ControlBits: #ctype unpacking
      control_bits.append(cbit == b'1')
    
    march = Microarchitectural_state(
      AluOut=self.AluOut.value,
      AluOpcode=self.AluOpcode.value,
      CarryIn=self.CarryIn.value,
      InstructionRegister=self.InstructionRegister.value,
      OperandRegister=self.OperandRegister.value,
      State=self.State.value,
      ControlBits=control_bits.copy())

    del control_bits

    self.TraceVector.append((arch,march))

  def step_n(self,Ncyc):
    N = Ncyc
    while(N>0):
      self.Barrier2.wait()
      self.trace_vector_append()
      self.Barrier1.wait()
      N = N-1
    # self.Kill.value  = 1
    # print(self.Barrier2.n_waiting)
    # self.Barrier2.wait()
    #Barrier2.wait()
    #print("End Cycle")

  def end_emulation(self):
    self.Kill.value  = 1
    self.Barrier2.wait()
    #Join threads and Prepare for Exit
    self.ThrCCG.join()
    self.ThrIR.join()
    self.ThrPC.join()
    self.ThrMEM.join()
    self.ThrRegArr.join()
    self.ThrALU.join()
    self.ThrSPtr.join()
    self.ThrOpReg.join()
    self.ThrIO.join()
    
    # self.DataBus.close()
    while(not self.DataBus.empty()):
      self.DataBus.get()
    # self.DataBus.join_thread()

    # self.IR_CCG.close()
    while(not self.IR_CCG.empty()):
      self.IR_CCG.get()
    # self.IR_CCG.join_thread()

    #print("No issue in init :D")
    # print (self.TraceVector)

if __name__ == '__main__':
  #mpl = multiprocessing.log_to_stderr()
  #mpl.setLevel(logging.DEBUG)
  main()