from abc import ABC, abstractmethod
import sys

###### State Definitions and abstract classes
## TODO Make the emulator io and emulator backend abstract classes so that they can be replaced with real hardware.

## RNBIP Architectural State
class Architectural_state():
  def __init__(self,PC,SP,Registers,Flags,Memory,IO_In,IO_Out):
    self.PC = PC
    self.SP = SP
    self.Registers = Registers
    self.Flags = Flags
    self.Memory = Memory
    self.IO_In = IO_In
    self.IO_Out = IO_Out

## RNBIP MicroArchitectural State
class Microarchitectural_state():
  def __init__(self,AluOut,AluOpcode,CarryIn,InstructionRegister,OperandRegister,State,ControlBits):
    self.AluOut = AluOut
    self.AluOpcode = AluOpcode
    self.CarryIn = CarryIn
    self.InstructionRegister = InstructionRegister
    self.OperandRegister = OperandRegister
    self.State = State
    self.ControlBits = ControlBits

## Emulator Components


## Look Up Tables for Compiler Passes.

def assembly2IR_LUT(x):
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
	}.get(x,"CHECK_LITERAL")

def IR2Binary_LUT(x):
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

def Hex2Bin_LUT(x):
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

def prettyPrintOpDecode(x):
      return {0:"NOP",
        1:"CLR",
        2:"CLC",
        3:"JUD <od>",
        4:"JUA ",
        5:"CUD <od>",
        6:"CUA ",
        7:"RTU",
        8:"JCD Z  <od>",
        9:"JCD NZ <od>",
        10:"JCD C <od>",
        11:"JCD NC <od>",
        12:"JCD P <od>",
        13:"JCD N <od>",
        14:"JCD OP <od>",
        15:"JCD EP <od>",
        16:"LSP ",
        17:"MVD R1",
        18:"MVD R2",
        19:"MVD R3",
        20:"MVD R4",
        21:"MVD R5",
        22:"MVD R6",
        23:"MVD R7",
        24:"RSP",
        25:"MVS R1",
        26:"MVS R2",
        27:"MVS R3",
        28:"MVS R4",
        29:"MVS R5",
        30:"MVS R6",
        31:"MVS R7",
        32:"NOT R0",
        33:"NOT R1",
        34:"NOT R2",
        35:"NOT R3",
        36:"NOT R4",
        37:"NOT R5",
        38:"NOT R6",
        39:"NOT R7",
        40:"JCA Z ",
        41:"JCA NZ",
        42:"JCA C ",
        43:"JCA NC",
        44:"JCA P ",
        45:"JCA N ",
        46:"JCA OP",
        47:"JCA EP",
        48:"CCD Z <od>",
        49:"CCD NZ <od>",
        50:"CCD C <od>",
        51:"CCD NC <od>",
        52:"CCD P <od>",
        53:"CCD N <od>",
        54:"CCD OP <od>",
        55:"CCD EP <od>",
        56:"CCA Z ",
        57:"CCA NZ",
        58:"CCA C ",
        59:"CCA NC",
        60:"CCA P ",
        61:"CCA N ",
        62:"CCA OP",
        63:"CCA EP",
        64:"INC R0",
        65:"INC R1",
        66:"INC R2",
        67:"INC R3",
        68:"INC R4",
        69:"INC R5",
        70:"INC R6",
        71:"INC R7",
        72:"RTC Z ",
        73:"RTC NZ",
        74:"RTC C ",
        75:"RTC NC",
        76:"RTC P ",
        77:"RTC N ",
        78:"RTC OP",
        79:"RTC EP",
        80:"DCR R0",
        81:"DCR R1",
        82:"DCR R2",
        83:"DCR R3",
        84:"DCR R4",
        85:"DCR R5",
        86:"DCR R6",
        87:"DCR R7",
        88:"MVI R0 <od>",
        89:"MVI R1 <od>",
        90:"MVI R2 <od>",
        91:"MVI R3 <od>",
        92:"MVI R4 <od>",
        93:"MVI R5 <od>",
        94:"MVI R6 <od>",
        95:"MVI R7 <od>",
        96:"RLA",
        97:"STA R1",
        98:"STA R2",
        99:"STA R3",
        100:"STA R4",
        101:"STA R5",
        102:"STA R6",
        103:"STA R7",
        104:"PSH R0",
        105:"PSH R1",
        106:"PSH R2",
        107:"PSH R3",
        108:"PSH R4",
        109:"PSH R5",
        110:"PSH R6",
        111:"PSH R7",
        112:"RRA",
        113:"LDA R1",
        114:"LDA R2",
        115:"LDA R3",
        116:"LDA R4",
        117:"LDA R5",
        118:"LDA R6",
        119:"LDA R7",
        120:"POP R0",
        121:"POP R1",
        122:"POP R2",
        123:"POP R3",
        124:"POP R4",
        125:"POP R5",
        126:"POP R6",
        127:"POP R7",
        128:"ADA R0",
        129:"ADA R1",
        130:"ADA R2",
        131:"ADA R3",
        132:"ADA R4",
        133:"ADA R5",
        134:"ADA R6",
        135:"ADA R7",
        136:"ADI R0 <od>",
        137:"ADI R1 <od>",
        138:"ADI R2 <od>",
        139:"ADI R3 <od>",
        140:"ADI R4 <od>",
        141:"ADI R5 <od>",
        142:"ADI R6 <od>",
        143:"ADI R7 <od>",
        144:"SBA R0",
        145:"SBA R1",
        146:"SBA R2",
        147:"SBA R3",
        148:"SBA R4",
        149:"SBA R5",
        150:"SBA R6",
        151:"SBA R7",
        152:"SBI R0 <od>",
        153:"SBI R1 <od>",
        154:"SBI R2 <od>",
        155:"SBI R3 <od>",
        156:"SBI R4 <od>",
        157:"SBI R5 <od>",
        158:"SBI R6 <od>",
        159:"SBI R7 <od>",
        160:"ACA R0",
        161:"ACA R1",
        162:"ACA R2",
        163:"ACA R3",
        164:"ACA R4",
        165:"ACA R5",
        166:"ACA R6",
        167:"ACA R7",
        168:"ACI R0 <od>",
        169:"ACI R1 <od>",
        170:"ACI R2 <od>",
        171:"ACI R3 <od>",
        172:"ACI R4 <od>",
        173:"ACI R5 <od>",
        174:"ACI R6 <od>",
        175:"ACI R7 <od>",
        176:"SCA R0",
        177:"SCA R1",
        178:"SCA R2",
        179:"SCA R3",
        180:"SCA R4",
        181:"SCA R5",
        182:"SCA R6",
        183:"SCA R7",
        184:"SCI R0 <od>",
        185:"SCI R1 <od>",
        186:"SCI R2 <od>",
        187:"SCI R3 <od>",
        188:"SCI R4 <od>",
        189:"SCI R5 <od>",
        190:"SCI R6 <od>",
        191:"SCI R7 <od>",
        192:"ANA R0",
        193:"ANA R1",
        194:"ANA R2",
        195:"ANA R3",
        196:"ANA R4",
        197:"ANA R5",
        198:"ANA R6",
        199:"ANA R7",
        200:"ANI R0 <od>",
        201:"ANI R1 <od>",
        202:"ANI R2 <od>",
        203:"ANI R3 <od>",
        204:"ANI R4 <od>",
        205:"ANI R5 <od>",
        206:"ANI R6 <od>",
        207:"ANI R7 <od>",
        208:"ORA R0",
        209:"ORA R1",
        210:"ORA R2",
        211:"ORA R3",
        212:"ORA R4",
        213:"ORA R5",
        214:"ORA R6",
        215:"ORA R7",
        216:"ORI R0 <od>",
        217:"ORI R1 <od>",
        218:"ORI R2 <od>",
        219:"ORI R3 <od>",
        220:"ORI R4 <od>",
        221:"ORI R5 <od>",
        222:"ORI R6 <od>",
        223:"ORI R7 <od>",
        224:"XRA R0",
        225:"XRA R1",
        226:"XRA R2",
        227:"XRA R3",
        228:"XRA R4",
        229:"XRA R5",
        230:"XRA R6",
        231:"XRA R7",
        232:"XRI R0 <od>",
        233:"XRI R1 <od>",
        234:"XRI R2 <od>",
        235:"XRI R3 <od>",
        236:"XRI R4 <od>",
        237:"XRI R5 <od>",
        238:"XRI R6 <od>",
        239:"XRI R7 <od>",
        240:"INA P0",
        241:"INA P1",
        242:"INA P2",
        243:"INA P3",
        244:"INA P4",
        245:"INA P5",
        246:"INA P6",
        247:"INA P7",
        248:"OUT P0",
        249:"OUT P1",
        250:"OUT P2",
        251:"OUT P3",
        252:"OUT P4",
        253:"OUT P5",
        254:"OUT P6",
        255:"OUT P7"}.get(x,"Error Decodeing Please Report")
