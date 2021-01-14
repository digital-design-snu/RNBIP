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

import time
from multiprocessing import Process


# 	Initialising & Instantiating inter module Signals
killthr = 0
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
IR_Reg = 0
ControlWord = 0 # init the fetch bit
MacState = 0 # init to fetch
S_AF = 0
GoFetch = 1
State = 0
FL = 0
Sel_Bits = 0

ALU_out = 0
Cout =  0
Zero = 0
Positive =0
OddParity= 0


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
blockMem= [] * 256
MEMConfFile = open('machCode.bin')
while(counter<256):
	line = MEMConfFile.readline()
	blockMem.append(int(line,2))
	counter = counter+1
counter = 0
while(counter<256):
	print(blockMem[counter])
	counter = counter+1
#Segment Ends
#this Segment of code Sets up the Register Array
counter=0
Reg_Array= [] * 8
while(counter<8):
	Reg_Array.append(counter)
	counter = counter+1
#Segment Ends
#this Segment of code Sets up the OUTPUT Array
counter=0
IO_Array= [] * 8
while(counter<8):
	IO_Array.append(0)
	counter = counter+1
#Segment Ends
#this Segment of code Sets up the INPUT Array
counter=0
IN_Array= [] * 8
while(counter<8):
	IN_Array.append(0)
	counter = counter+1
#Segment Ends
#this Segment of code Sets up the Flag Array
counter=0
Flag_Array= [] * 8
while(counter<8):
	Flag_Array.append(counter&1)
	counter = counter+1
#Segment Ends

#this Segment of code Sets up the Flag Array
OutPutFile =  open('MachineState.var','w')
#Segment Ends

#this Segment Populates the Control Code Generator 
ControlCodeArr = [0] *512
def initCCG():
    global ControlCodeArr
    ControlCodeArr[ 0 ]     =    int('1010010000100000000000',2) #    Fetch    
    ControlCodeArr[ 1 ]     =    int('0000000000001000000000',2) #    NOP    
    ControlCodeArr[ 2 ]     =    int('0000000000001000011010',2) #    CLR    
    ControlCodeArr[ 4 ]     =    int('0000000000001000010000',2) #    CLC    
    ControlCodeArr[ 6 ]     =    int('1010000000000000100000',2) #    JUD <od>
    ControlCodeArr[ 7 ]     =    int('0000001000001001000000',2) #        
    ControlCodeArr[ 8 ]     =    int('0000001000001000000100',2) #    JUA     
    ControlCodeArr[ 10 ]    =    int('0101100010000000000000',2) #    CUD <od>
    ControlCodeArr[ 11 ]    =    int('1010001000001000000000',2) #       
    ControlCodeArr[ 12 ]    =    int('0101100010000000000000',2) #    CUA 
    ControlCodeArr[ 13 ]    =    int('0000001000001000000100',2) #        
    ControlCodeArr[ 14 ]    =    int('1001001001001000000000',2) #    RTU    
    ControlCodeArr[ 16 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 17 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 18 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 19 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 20 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 21 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 22 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 23 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 24 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 25 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 26 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 27 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 28 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 29 ]    =    int('0000001000001001000000',2) #    
    ControlCodeArr[ 30 ]    =    int('1010010000011000100000',2) #    JCD <fl><od>
    ControlCodeArr[ 31 ]    =    int('0000001000001001000000',2) #        
    ControlCodeArr[ 32 ]    =    int('0000000011001000000100',2) #    LSP     
    ControlCodeArr[ 34 ]    =    int('0000000000001000000110',2) #    MVD <rn>*
    ControlCodeArr[ 36 ]    =    int('0000000000001000000110',2) #    MVD <rn>*
    ControlCodeArr[ 38 ]    =    int('0000000000001000000110',2) #    MVD <rn>*
    ControlCodeArr[ 40 ]    =    int('0000000000001000000110',2) #    MVD <rn>*
    ControlCodeArr[ 42 ]    =    int('0000000000001000000110',2) #    MVD <rn>*
    ControlCodeArr[ 44 ]    =    int('0000000000001000000110',2) #    MVD <rn>*
    ControlCodeArr[ 46 ]    =    int('0000000000001000000110',2) #    MVD <rn>*    
    ControlCodeArr[ 48 ]    =    int('0000000100001000001000',2) #    RSP    
    ControlCodeArr[ 50 ]    =    int('0000000000001000001001',2) #    MVS <rn>*
    ControlCodeArr[ 52 ]    =    int('0000000000001000001001',2) #    MVS <rn>*
    ControlCodeArr[ 54 ]    =    int('0000000000001000001001',2) #    MVS <rn>*
    ControlCodeArr[ 56 ]    =    int('0000000000001000001001',2) #    MVS <rn>*
    ControlCodeArr[ 58 ]    =    int('0000000000001000001001',2) #    MVS <rn>*
    ControlCodeArr[ 60 ]    =    int('0000000000001000001001',2) #    MVS <rn>*
    ControlCodeArr[ 62 ]    =    int('0000000000001000001001',2) #    MVS <rn>*    
    ControlCodeArr[ 64 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 65 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 66 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 67 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 68 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 69 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 70 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 71 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 72 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 73 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 74 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 75 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 76 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 77 ]    =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 78 ]    =    int('0000000000000000100001',2) #    NOT <rn>
    ControlCodeArr[ 79 ]    =    int('0000000000001001010010',2) #        
    ControlCodeArr[ 80 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 81 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 82 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 83 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 84 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 85 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 86 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 87 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 88 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 89 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 90 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 91 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 92 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 93 ]    =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 94 ]    =    int('0000000000011000100100',2) #    JCA <fl>
    ControlCodeArr[ 95 ]    =    int('0000011000001000000000',2) #        
    ControlCodeArr[ 96 ]    =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 97 ]    =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 98 ]    =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 99 ]    =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 100 ]   =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 101 ]   =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 102 ]   =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 103 ]   =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 104 ]   =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 105 ]   =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 106 ]   =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 107 ]   =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 108 ]   =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 109 ]   =    int('0101111010001000000000',2) #    
    ControlCodeArr[ 110 ]   =    int('1010010000011000100000',2) #    CCD <fl><od>
    ControlCodeArr[ 111 ]   =    int('0101111010001000000000',2) #       
    ControlCodeArr[ 112 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 113 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 114 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 115 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 116 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 117 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 118 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 119 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 120 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 121 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 122 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 123 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 124 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 125 ]   =    int('0000001000001000000100',2) #
    ControlCodeArr[ 126 ]   =    int('0101100010011000000000',2) #    CCA <fl>
    ControlCodeArr[ 127 ]   =    int('0000001000001000000100',2) #    
    ControlCodeArr[ 128 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 129 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 130 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 131 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 132 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 133 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 134 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 135 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 136 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 137 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 138 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 139 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 140 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 141 ]   =    int('0000000000001001010010',2) #
    ControlCodeArr[ 142 ]   =    int('0000000000000000100001',2) #    INC <rn>
    ControlCodeArr[ 143 ]   =    int('0000000000001001010010',2) #        
    ControlCodeArr[ 144 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 145 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 146 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 147 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 148 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 149 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 150 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 151 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 152 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 153 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 154 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 155 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 156 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 157 ]   =    int('0000011000001000000000',2) #    
    ControlCodeArr[ 158 ]   =    int('1001000001011000100000',2) #    RTC <fl>
    ControlCodeArr[ 159 ]   =    int('0000011000001000000000',2) #        
    ControlCodeArr[ 160 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 161 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 162 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 163 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 164 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 165 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 166 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 167 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 168 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 169 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 170 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 171 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 172 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 173 ]   =    int('0000000000001001010010',2) #    
    ControlCodeArr[ 174 ]   =    int('0000000000000000100001',2) #    DCR <rn>
    ControlCodeArr[ 175 ]   =    int('0000000000001001010010',2) #        
    ControlCodeArr[ 176 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 178 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 180 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 182 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 184 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 186 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 188 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>
    ControlCodeArr[ 190 ]   =    int('1010010000001000000010',2) #    MVI <rn><od>    
    ControlCodeArr[ 192 ]   =    int('0000000000000000100100',2) #    RLA
    ControlCodeArr[ 193 ]   =    int('0000000000001001011000',2) #        
    ControlCodeArr[ 194 ]   =    int('0100000000001000000001',2) #    STA <rn>*
    ControlCodeArr[ 196 ]   =    int('0100000000001000000001',2) #    STA <rn>*
    ControlCodeArr[ 198 ]   =    int('0100000000001000000001',2) #    STA <rn>*
    ControlCodeArr[ 200 ]   =    int('0100000000001000000001',2) #    STA <rn>*
    ControlCodeArr[ 202 ]   =    int('0100000000001000000001',2) #    STA <rn>*
    ControlCodeArr[ 204 ]   =    int('0100000000001000000001',2) #    STA <rn>*
    ControlCodeArr[ 206 ]   =    int('0100000000001000000001',2) #    STA <rn>*    
    ControlCodeArr[ 208 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 210 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 212 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 214 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 216 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 218 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 220 ]   =    int('0101000010001000000001',2) #    PSH <rn>
    ControlCodeArr[ 222 ]   =    int('0101000010001000000001',2) #    PSH <rn>    
    ControlCodeArr[ 224 ]   =    int('0000000000000000100100',2) #     RRA
    ControlCodeArr[ 225 ]   =    int('0000000000001001011000',2) #        
    ControlCodeArr[ 226 ]   =    int('1000000000001000000010',2) #    LDA <rn>*
    ControlCodeArr[ 228 ]   =    int('1000000000001000000010',2) #    LDA <rn>*
    ControlCodeArr[ 230 ]   =    int('1000000000001000000010',2) #    LDA <rn>*
    ControlCodeArr[ 232 ]   =    int('1000000000001000000010',2) #    LDA <rn>*
    ControlCodeArr[ 234 ]   =    int('1000000000001000000010',2) #    LDA <rn>*
    ControlCodeArr[ 236 ]   =    int('1000000000001000000010',2) #    LDA <rn>*
    ControlCodeArr[ 238 ]   =    int('1000000000001000000010',2) #    LDA <rn>*    
    ControlCodeArr[ 240 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 242 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 244 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 246 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 248 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 250 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 252 ]   =    int('1001000001001000000010',2) #    POP <rn>
    ControlCodeArr[ 254 ]   =    int('1001000001001000000010',2) #    POP <rn>    
    ControlCodeArr[ 256 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 257 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 258 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 259 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 260 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 261 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 262 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 263 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 264 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 265 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 266 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 267 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 268 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 269 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 270 ]   =    int('0000000000000000100100',2) #    ADA <rn>
    ControlCodeArr[ 271 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 272 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 273 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 274 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 275 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 276 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 277 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 278 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 279 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 280 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 281 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 282 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 283 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 284 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 285 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 286 ]   =    int('0000000000000000100001',2) #    ADI <rn><od>
    ControlCodeArr[ 287 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 288 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 289 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 290 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 291 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 292 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 293 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 294 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 295 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 296 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 297 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 298 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 299 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 300 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 301 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 302 ]   =    int('0000000000000000100100',2) #    SBA <rn>
    ControlCodeArr[ 303 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 304 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 305 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 306 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 307 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 308 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 309 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 310 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 311 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 312 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 313 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 314 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 315 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 316 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 317 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 318 ]   =    int('0000000000000000100001',2) #    SBI <rn><od>
    ControlCodeArr[ 319 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 320 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 321 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 322 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 323 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 324 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 325 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 326 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 327 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 328 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 329 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 330 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 331 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 332 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 333 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 334 ]   =    int('0000000000000000100100',2) #    ACA <rn>
    ControlCodeArr[ 335 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 336 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 337 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 338 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 339 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 340 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 341 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 342 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 343 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 344 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 345 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 346 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 347 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 348 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 349 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 350 ]   =    int('0000000000000000100001',2) #    ACI <rn><od>
    ControlCodeArr[ 351 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 352 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 353 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 354 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 355 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 356 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 357 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 358 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 359 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 360 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 361 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 362 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 363 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 364 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 365 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 366 ]   =    int('0000000000000000100100',2) #    SCA <rn>
    ControlCodeArr[ 367 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 368 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 369 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 370 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 371 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 372 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 373 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 374 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 375 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 376 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 377 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 378 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 379 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 380 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 381 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 382 ]   =    int('0000000000000000100001',2) #    SCI <rn><od>
    ControlCodeArr[ 383 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 384 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 385 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 386 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 387 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 388 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 389 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 390 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 391 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 392 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 393 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 394 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 395 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 396 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 397 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 398 ]   =    int('0000000000000000100100',2) #    ANA <rn>
    ControlCodeArr[ 399 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 400 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 401 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 402 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 403 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 404 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 405 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 406 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 407 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 408 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 409 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 410 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 411 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 412 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 413 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 414 ]   =    int('0000000000000000100001',2) #    ANI <rn><od>
    ControlCodeArr[ 415 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 416 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 417 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 418 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 419 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 420 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 421 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 422 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 423 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 424 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 425 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 426 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 427 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 428 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 429 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 430 ]   =    int('0000000000000000100100',2) #    ORA <rn>
    ControlCodeArr[ 431 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 432 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 433 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 434 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 435 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 436 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 437 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 438 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 439 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 440 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 441 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 442 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 443 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 444 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 445 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 446 ]   =    int('0000000000000000100001',2) #    ORI <rn><od>
    ControlCodeArr[ 447 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 448 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 449 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 450 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 451 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 452 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 453 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 454 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 455 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 456 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 457 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 458 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 459 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 460 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 461 ]   =    int('0000000000001000011001',2) #    
    ControlCodeArr[ 462 ]   =    int('0000000000000000100100',2) #    XRA <rn>
    ControlCodeArr[ 463 ]   =    int('0000000000001000011001',2) #        
    ControlCodeArr[ 464 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 465 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 466 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 467 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 468 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 469 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 470 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 471 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 472 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 473 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 474 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 475 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 476 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 477 ]   =    int('1010010000001000010010',2) #    
    ControlCodeArr[ 478 ]   =    int('0000000000000000100001',2) #    XRI <rn><od>
    ControlCodeArr[ 479 ]   =    int('1010010000001000010010',2) #        
    ControlCodeArr[ 480 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 482 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 484 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 486 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 488 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 490 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 492 ]   =    int('0000000000001100001000',2) #    INA <pn>
    ControlCodeArr[ 494 ]   =    int('0000000000001100001000',2) #    INA <pn>    
    ControlCodeArr[ 496 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 498 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 500 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 502 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 504 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 506 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 508 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    ControlCodeArr[ 510 ]   =    int('0000000000001010000100',2) #    OUT <pn>
    return
initCCG()
#Segment Ends

# 	Instantiating Functional blocks of the Architecture 
def BusArbt():
	global killthr
	global RD,E_PC,E_SP
	global E_R0,E_RN,E_OR,E_IP
	global dataBus,PC_reg
	global MEMOut,SPOut,IOOut,OROut,RAOut
	while(killthr):
		if(RD): dataBus	= MEMOut
		elif(E_PC): dataBus = PC_reg  
		elif(E_SP): dataBus = SP_Address  
		elif(E_IP): dataBus = IOOut 
		elif(E_OR): dataBus = OperandReg 
		elif( E_R0 | E_RN): dataBus	= RAOut
		else: dataBus = 0
	return
	
#Memory Module
def Mem():
	global killthr,posedgeClk
	global WR,blockMem
	global dataBus,Address_Bus
	while(killthr):
		while(posedgeClk):
			if(WR):	blockMem[Address_Bus] = dataBus
			#add some gate delay ?
	return

def Alu():
	global killthr
	global dataBus,OperandReg,S_AF
	global ALU_RN,ALU_FR,ALU_FR_Carry
	global ALU_out,Cout,Zero,Positive,OddParity
	while(killthr):
		if   (S_AF== 0    ):  ALU_imOut = 0                            
		elif (S_AF== 1    ):  ALU_imOut = dataBus                
		elif (S_AF== 2    ):  ALU_imOut = (~dataBus & 0xFF)          
		elif (S_AF== 3    ):  ALU_imOut = OperandReg                          
		elif (S_AF== 4    ):  ALU_imOut = dataBus+1                  
		elif (S_AF== 5    ):  ALU_imOut = dataBus-1                  
		elif (S_AF== 6    ):  ALU_imOut = (dataBus<<1+Cin)           
		elif (S_AF== 7    ):  ALU_imOut = (((dataBus%2)<<8)+(Cin<<7)+(dataBus>>1))   
		elif (S_AF== 8    ):  ALU_imOut = dataBus+OperandReg                   
		elif (S_AF== 9    ):  ALU_imOut = OperandReg-dataBus                   
		elif (S_AF== 10   ):  ALU_imOut = dataBus+OperandReg+Cin           
		elif (S_AF== 11   ):  ALU_imOut = OperandReg-dataBus-Cin           
		elif (S_AF== 12   ):  ALU_imOut = dataBus&OperandReg                  
		elif (S_AF== 13   ):  ALU_imOut = dataBus|OperandReg                  
		elif (S_AF== 14   ):  ALU_imOut = dataBus^OperandReg                  
		elif (S_AF== 15   ):  ALU_imOut = ~(dataBus^OperandReg) & 0xFF
		ALU_out = ALU_imOut%256
		Cout =  ALU_imOut/256
		Zero = (ALU_out == 0);
		Positive = ~(ALU_out&(1<<7));
		OddParity ^= ALU_out;
	return

#Alu

#Address Selector
def AddressSel():
	global killthr
	global S_SP,S_PC,PC_reg,SP_Address,Address_Bus
	while(killthr):
		if  (S_PC) :  Address_Bus = PC_reg
		elif(S_SP) :  Address_Bus = SP_Address
		else: Address_Bus = Reg_Array[0]
	return

#Program Counter
def ProgramCounter():
	global killthr,posedgeClk
	global I_PC,L_PC,dataBus,PC_reg,OperandReg
	while(killthr):
		while(posedgeClk):
			if  (I_PC == 0 and L_PC == 0) :  PC_reg = PC_reg
			elif(I_PC == 1 and L_PC == 0) :  PC_reg = (PC_reg + 1)%256
			elif(I_PC == 0 and L_PC == 1) :  PC_reg = dataBus
			else:PC_reg = OperandReg
	return
	
#Instruction Register
def InstReg():
	global killthr
	global L_IR,dataBus,IR_Reg
	while(killthr):
		if(L_IR):
			IR_Reg = dataBus
	return
	
	
def OperandRegister():
	global killthr,posedgeClk
	global L_OR,dataBus,OperandReg
	while(killthr):
		while(posedgeClk):
			if(L_OR):
				OperandReg = dataBus	
	return
#Operand Register

#Control Code Generator

#block that updates the state bit
def ControlCodeGeneratorT1():
	global killthr,posedgeClk,State,GoFetch
	while(killthr):
		while(posedgeClk):
			if(GoFetch):
				State = 0
			else:
				State =(State + 1)%2 # not that the %2 is necessary 
	return
#Block that Updates the Control Codes
def ControlCodeGeneratorT2():
	global killthr,posedgeClk,State,IR_Reg,ControlCodeArr
	global S_SP,S_PC,RD,WR,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,S_AL
	global L_R0,L_RN,E_R0,E_RN,E_OR,L_OR,E_IP,L_OP,E_FL,S_IF,GoFetch
	while(killthr):
		while(posedgeClk):
			if(not GoFetch):
				MacState = (IR_Reg<<1)+State
			elif(GoFetch):
				MacState = 0
			elif(IR_Reg == 00) :
				MacState = 1
			ControlWord = ControlCodeArr[MacState]
			RD		= 1 if((ControlWord & 1<<21   )>0) else 0 	
			WR		= 1 if((ControlWord & 1<<20	  )>0) else 0
			S_PC	= 1 if((ControlWord & 1<<19   )>0) else 0
			S_SP	= 1 if((ControlWord & 1<<18   )>0) else 0
			E_PC	= 1 if((ControlWord & 1<<17   )>0) else 0
			I_PC	= 1 if((ControlWord & 1<<16   )>0) else 0
			L_PC	= 1 if((ControlWord & 1<<15   )>0) else 0
			E_SP	= 1 if((ControlWord & 1<<14   )>0) else 0
			D_SP	= 1 if((ControlWord & 1<<13   )>0) else 0
			I_SP	= 1 if((ControlWord & 1<<12   )>0) else 0
			L_IR	= 1 if((ControlWord & 1<<11   )>0) else 0
			E_FL	= 1 if((ControlWord & 1<<10   )>0) else 0
			S_IF	= 1 if((ControlWord & 1<<9    )>0) else 0
			E_IP	= 1 if((ControlWord & 1<<8    )>0) else 0
			L_OP	= 1 if((ControlWord & 1<<7    )>0) else 0
			E_OR	= 1 if((ControlWord & 1<<6    )>0) else 0
			L_OR	= 1 if((ControlWord & 1<<5    )>0) else 0
			S_AL	= 1 if((ControlWord & 1<<4    )>0) else 0
			L_R0	= 1 if((ControlWord & 1<<3    )>0) else 0
			E_R0	= 1 if((ControlWord & 1<<2    )>0) else 0
			L_RN	= 1 if((ControlWord & 1<<1    )>0) else 0
			E_RN	= 1 if((ControlWord & 1<<0    )>0) else 0
	return
#Block that Sets the Fetch Flag High
def ControlCodeGeneratorT3():
	global killthr,posedgeClk,State,GoFetch,E_FL,FL,S_IF
	while(killthr):
		GoFetch = ((not (E_FL and FL)) and S_IF);
	return
	
#Register Array
def RegisterAr():	
	global killthr,posedgeClk,ALU_out
	global L_R0,L_RN,E_R0,E_RN,S_AL
	global dataBus,Sel_Bits,Reg_Array
	while(killthr):
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
			elif(L_RN):	Reg_Array[Sel_Bits] = ALU_out if (S_AL) else dataBus;
	return

#Flag Array	
def FlagArray():
	global killthr,posedgeClk
	global S_SP,S_PC,RD,WR,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,S_AL
	global L_R0,L_RN,E_R0,E_RN,E_OR,L_OR,E_IP,L_OP,E_FL,S_IF
	global dataBus,PC_reg,OperandReg,SP_Address,S_AF,GoFetch,Flag_Array
	global OR_ALU,SP_AS,PC_AS,R0_AS,ALU_RN,opcode,OR_PC,ALU_FR,ALU_FR_Carry,FR_CG
	global E_FLi,S_IFi,PCOut,MEMOut,OROut,SPOut,RAOut,IOOut,ioOut0,Address_Bus
	#need to write flag reg
	return

#Stack Pointer
def StackPointer():
	global killthr,posedgeClk
	global E_SP,D_SP,I_SP,dataBus,SP_Address
	while(killthr):
		while(posedgeClk):
			if(I_SP == 0 and D_SP == 0) :  SP_Address = SP_Address
			elif(I_SP == 1 and D_SP == 0) :  SP_Address = (SP_Address + 1)%256
			elif(I_SP == 0 and D_SP == 1) :  SP_Address = (SP_Address - 1)%256
			else:SP_Address = dataBus
	return
	
def IO_Module():	
	global killthr,posedgeClk
	global L_OP,dataBus,IO_Array,Sel_Bits
	while(killthr):
		while(posedgeClk):
			if(L_OP):	IO_Array[Sel_Bits] =  dataBus;
	return

#continually Driven Signals
def CtSigDrv():
	global killthr,posedgeClk,Reg_Array,Sel_Bits,blockMem
	global S_SP,S_PC,RD,WR,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,S_AL
	global L_R0,L_RN,E_R0,E_RN,E_OR,L_OR,E_IP,L_OP,E_FL,S_IF
	global dataBus,PC_reg,OperandReg,SP_Address,S_AF,GoFetch
	global OR_ALU,SP_AS,PC_AS,R0_AS,ALU_RN,opcode,OR_PC,ALU_FR,ALU_FR_Carry,FR_CG
	global E_FLi,S_IFi,PCOut,MEMOut,OROut,SPOut,RAOut,IOOut,ioOut0,Address_Bus
	while(killthr):
		E_FLi = E_FL
		S_IFi = S_IF
		SP_Address = (SP_Address-1) if D_SP else SP_Address
		S_AF = (IR_Reg/16)
		Sel_Bits = (IR_Reg%8)
		MEMOut = blockMem[Address_Bus]
		OR_Out = OperandReg
		IO_Out = IN_Array[Sel_Bits]
		RA_Out = Reg_Array[0] if (E_R0) else Reg_Array[Sel_Bits] 
	return

#The Top Clock Module and Output File printing module
def TopModule():
	global LoopCounter,OutPutFile
	global killthr,posedgeClk
	global S_SP,S_PC,RD,WR,E_PC,I_PC,L_PC,E_SP,D_SP,I_SP,L_IR,S_AL
	global L_R0,L_RN,E_R0,E_RN,E_OR,L_OR,E_IP,L_OP,E_FL,S_IF
	global dataBus,PC_reg,OperandReg,SP_Address,S_AF,GoFetch
	global OR_ALU,SP_AS,PC_AS,R0_AS,ALU_RN,opcode,OR_PC,ALU_FR,ALU_FR_Carry,FR_CG
	global E_FLi,S_IFi,PCOut,MEMOut,OROut,SPOut,RAOut,IOOut,ioOut0,Address_Bus
	while(LoopCounter<100):
	#issue posedge
		posedgeClk = 1
		time.sleep(0.001)
	#kill posedge
		posedgeClk = 0
		time.sleep(0.00001)
	#write state into vis driver file
		OutPutFile.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (LoopCounter,dataBus,MEMOut,PC_reg,SP_Address,IOOut,OperandReg,RAOut))
		
		
		LoopCounter = LoopCounter + 1
	#loop
	return
	
LoopCounter = 0
killthr = 1 # a negative logic flag 
print("This Executes till Here :)")
	
ThrBusArbt                    =Process(target =BusArbt)               
ThrMem                        =Process(target =Mem)                   
ThrAlu                        =Process(target =Alu)                   
ThrAddressSel                 =Process(target =AddressSel)            
ThrProgramCounter             =Process(target =ProgramCounter)        
ThrInstReg                    =Process(target =InstReg)               
ThrOperandRegister            =Process(target =OperandRegister)       
ThrControlCodeGeneratorT1     =Process(target =ControlCodeGeneratorT1)
ThrControlCodeGeneratorT2     =Process(target =ControlCodeGeneratorT2)
ThrControlCodeGeneratorT3     =Process(target =ControlCodeGeneratorT3)
ThrRegisterAr                 =Process(target =RegisterAr)            
ThrFlagArray                  =Process(target =FlagArray)             
ThrStackPointer               =Process(target =StackPointer)          
ThrCtSigDrv                   =Process(target =CtSigDrv)              
ThrTopModule                  =Process(target =TopModule)             
ThrIO_Module                  =Process(target =IO_Module) 


ThrBusArbt.start()                   
ThrMem.start()                       
ThrAlu.start()                       
ThrAddressSel.start()                
ThrProgramCounter.start()            
ThrInstReg.start()                   
ThrOperandRegister.start()           
ThrControlCodeGeneratorT1.start()    
ThrControlCodeGeneratorT2.start()    
ThrControlCodeGeneratorT3.start()    
ThrRegisterAr.start()                
ThrFlagArray.start()                 
ThrStackPointer.start()              
ThrCtSigDrv.start()                  
ThrTopModule.start()                 
ThrIO_Module.start()                 

print("Threads Started")   
bob = 0
while(LoopCounter<100):
	bob = not bob
print("Issued Kill")

killthr = 0
time.sleep(0.001)
OutPutFile.close()
ThrBusArbt.join()                   
ThrMem.join()                       
ThrAlu.join()                       
ThrAddressSel.join()                
ThrProgramCounter.join()            
ThrInstReg.join()                   
ThrOperandRegister.join()           
ThrControlCodeGeneratorT1.join()    
ThrControlCodeGeneratorT2.join()    
ThrControlCodeGeneratorT3.join()    
ThrRegisterAr.join()                
ThrFlagArray.join()                 
ThrStackPointer.join()              
ThrCtSigDrv.join()                  
ThrTopModule.join()                 
ThrIO_Module.join() 
#start threads here

# Start top Module 

# Finish Up :)




	

