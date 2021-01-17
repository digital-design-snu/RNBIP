// Program 1: Loop till Carry
// 
// Clear
// OD to R6
// OD to R7
// R6 to R0
// R0 to R0+R7
// if Carry 
// 	PC = 0
// PC = 5
//----------
CLR
MVI R6 B1
MVI R7 0F
MVS R6
ADA R7
JCD C 00
JUD 06
//----------




// Program 2: Infinite Wave
// 
// Clear
// OD to R1
// OD to R2
// R1 to R0
// R0 to R7
// R2 to R0
// R0 to R0-R1
// R0 to R4
// INC R7
// DEC R0
// if R0=0
// 	R4 to R0
// DEC R7
// DEC R0
// 
// 
// 
// 
//----------
CLR
MVI R1 20
MVI R2 25
MVS R1
MVD R7
MVS R2
SBA R1
MVD R4
MVS R4
INC R7
DCR R0
JCD NZ 0B
MVS R4
DCR R7
DCR R0
JCD NZ 10
JUD 0A
//----------

// better:
//----------
CLR
MVI R1 20
MVI R2 30
MVS R1
MVD R7
MVS R2
SBA R1
MVD R4
INC R7
DCR R0
JCD NZ 0A
MVS R4
DCR R7
DCR R0
JCD NZ 0F
MVS R4
JUD 0A
//----------

// Program 3: Push PopCLR
MVI R1 B7
MVI R2 C7
MVI R3 D7
MVI R4 E7
PSH R1
PSH R2
PSH R3
PSH R4
CLR
POP R1
POP R2
POP R3
POP R4
//----------
CLR
MVI R1 B7
MVI R2 C7
MVI R3 D7
MVI R4 E7
PSH R1
PSH R2
PSH R3
PSH R4
CLR
POP R1
POP R2
POP R3
POP R4
//----------

// Program 4: Function Return 1 (Logical Operators)
// 
// Clear
// OD to R1
// OD to R2
// OD to R3
// CUD(Unconditional Br. OD to PC, store PC in SP)
// OD to R4
// OD to R5
// OD to R6
// CUD(Unconditional Br. OD2 to PC, store PC in SP)
// R0 to R0 ^ R7
// R0 to R7
// 
// @[OD]
// R1 to R0
// R0 to R0 | R2
// R0 to R0 | R3
// R0 to R7
// RTU
// 
// @[OD2]
// R4 to R0
// R0 to R0 & R5
// R0 to R0 & R6
// RTU
//----------
CLR
MVI R1 A5
MVI R2 B4
MVI R3 99
CUD 20
MVI R4 33
MVI R5 79
MVI R6 6F
CUD 30
XRA R7
MVD R7
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
MVS R1
ORA R2
ORA R3
MVD R7
RTU
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
NOP
MVS R4
ANA R5
ANA R6
RTU
//-------------------------------------------------------------------------------------------------------------------------------
