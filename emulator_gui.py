import sys
import os
import time
from RNBIP_ISA import prettyPrintOpDecode

from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QMainWindow, QTableWidgetItem,
    QDesktopWidget)
from PyQt5.QtGui import (QFont, QPixmap, QPalette)
from PyQt5.QtCore import (Qt, QRect,QPoint,QSize)

import MainWindow_UI

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True) 

### Global State
path = os.path.dirname(os.path.abspath(__file__))

### QT GUI MainWinDow
class MainWidow(QMainWindow):

  def __init__(self,inst_emulator,inst_assembler,*args, **kwargs):
    super().__init__(*args, **kwargs)
    self.constructor()
    
    # Emulator Interface Setup
    # Connect Buttons
    self.ui.nextStage.clicked.connect(self.on_nextStage_clicked)
    self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)
    self.ui.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
    self.ui.reset.clicked.connect(self.on_reset_clicked)
    self.ui.run10ClockCycle.clicked.connect(self.on_run10ClockCycle_clicked)

    self.inst_emulator = inst_emulator
    self.inst_emulator.start()
    self.inst_emulator.step_n(1)
    self.trace_index = 0
    self.last_compiled_mem = "00000000"
    self.log_string = "Welcome to the RNBIP Emulator \nEnter an Assembly program above and Hit the Compile button to get started !"
    self.ui.logBox.setText(self.log_string)
    self.inst_assembler = inst_assembler

  def constructor(self):
    self.ui = MainWindow_UI.Ui_MainWidow()
    self.ui.setupUi(self)
    
    self.setWindowTitle("Single-Bus Processor")
    self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    
    self.show()
    
    h = self.height()-100
    w = self.width()-500
    pix = QPixmap(os.path.join(path,"asset/back_final.png"))
    self.ui.imageLabel_Source.setPixmap(pix.scaled(w,h,Qt.KeepAspectRatio))

    pix_1 = QPixmap(os.path.join(path,"asset/RD.png"))
    self.ui.imageLabel.setPixmap(pix_1.scaled(w,h,Qt.KeepAspectRatio))

    pix_2 = QPixmap(os.path.join(path,"asset/WR.png"))
    self.ui.imageLabel_2.setPixmap(pix_2.scaled(w,h,Qt.KeepAspectRatio))

    pix_3 = QPixmap(os.path.join(path,"asset/S_PC.png"))
    self.ui.imageLabel_3.setPixmap(pix_3.scaled(w,h,Qt.KeepAspectRatio))

    pix_4 = QPixmap(os.path.join(path,"asset/S_SP.png"))
    self.ui.imageLabel_4.setPixmap(pix_4.scaled(w,h,Qt.KeepAspectRatio))

    pix_5 = QPixmap(os.path.join(path,"asset/E_PC.png"))
    self.ui.imageLabel_5.setPixmap(pix_5.scaled(w,h,Qt.KeepAspectRatio))

    pix_6 = QPixmap(os.path.join(path,"asset/I_PC.png"))
    self.ui.imageLabel_6.setPixmap(pix_6.scaled(w,h,Qt.KeepAspectRatio))

    pix_7 = QPixmap(os.path.join(path,"asset/L_PC.png"))
    self.ui.imageLabel_7.setPixmap(pix_7.scaled(w,h,Qt.KeepAspectRatio))

    pix_8 = QPixmap(os.path.join(path,"asset/E_SP.png"))
    self.ui.imageLabel_8.setPixmap(pix_8.scaled(w,h,Qt.KeepAspectRatio))

    pix_9 = QPixmap(os.path.join(path,"asset/D_SP.png"))
    self.ui.imageLabel_9.setPixmap(pix_9.scaled(w,h,Qt.KeepAspectRatio))

    pix_10 = QPixmap(os.path.join(path,"asset/I_SP.png"))
    self.ui.imageLabel_10.setPixmap(pix_10.scaled(w,h,Qt.KeepAspectRatio))

    pix_11 = QPixmap(os.path.join(path,"asset/L_IR.png"))
    self.ui.imageLabel_11.setPixmap(pix_11.scaled(w,h,Qt.KeepAspectRatio))

    pix_12 = QPixmap(os.path.join(path,"asset/E_FL.png"))
    self.ui.imageLabel_12.setPixmap(pix_12.scaled(w,h,Qt.KeepAspectRatio))

    pix_13 = QPixmap(os.path.join(path,"asset/S_IF.png"))
    self.ui.imageLabel_13.setPixmap(pix_13.scaled(w,h,Qt.KeepAspectRatio))

    pix_14 = QPixmap(os.path.join(path,"asset/E_IP.png"))
    self.ui.imageLabel_14.setPixmap(pix_14.scaled(w,h,Qt.KeepAspectRatio))

    pix_15 = QPixmap(os.path.join(path,"asset/L_OP.png"))
    self.ui.imageLabel_15.setPixmap(pix_15.scaled(w,h,Qt.KeepAspectRatio))

    pix_16 = QPixmap(os.path.join(path,"asset/E_OR.png"))
    self.ui.imageLabel_16.setPixmap(pix_16.scaled(w,h,Qt.KeepAspectRatio))

    pix_17 = QPixmap(os.path.join(path,"asset/L_OR.png"))
    self.ui.imageLabel_17.setPixmap(pix_17.scaled(w,h,Qt.KeepAspectRatio))

    pix_18 = QPixmap(os.path.join(path,"asset/S_AL.png"))
    self.ui.imageLabel_18.setPixmap(pix_18.scaled(w,h,Qt.KeepAspectRatio))

    pix_19 = QPixmap(os.path.join(path,"asset/L_R0.png"))
    self.ui.imageLabel_19.setPixmap(pix_19.scaled(w,h,Qt.KeepAspectRatio))

    pix_20 = QPixmap(os.path.join(path,"asset/E_R0.png"))
    self.ui.imageLabel_20.setPixmap(pix_20.scaled(w,h,Qt.KeepAspectRatio))

    pix_21 = QPixmap(os.path.join(path,"asset/L_RN.png"))
    self.ui.imageLabel_21.setPixmap(pix_21.scaled(w,h,Qt.KeepAspectRatio))

    pix_22 = QPixmap(os.path.join(path,"asset/E_RN.png"))
    self.ui.imageLabel_22.setPixmap(pix_22.scaled(w,h,Qt.KeepAspectRatio))

    pix_23 = QPixmap(os.path.join(path,"asset/Databus.png"))
    self.ui.imageLabel_23.setPixmap(pix_23.scaled(w,h,Qt.KeepAspectRatio))

    pix_24 = QPixmap(os.path.join(path,"asset/L_SP.png"))
    self.ui.imageLabel_24.setPixmap(pix_24.scaled(w,h,Qt.KeepAspectRatio))

    # killLRN =  QPixmap(os.path.join(path,"imgasset//killLRN.png"))
    # self.ui.imageLabel_25.setPixmap(killLRN.scaled(w,h,Qt.KeepAspectRatio))

    pix_26 = QPixmap(os.path.join(path,"asset/killLRN2.png"))
    self.ui.imageLabel_26.setPixmap(pix_26.scaled(w,h,Qt.KeepAspectRatio))

    pix_27 = QPixmap(os.path.join(path,"asset/killLR0.png"))
    self.ui.imageLabel_27.setPixmap(pix_27.scaled(w,h,Qt.KeepAspectRatio))

    pix_28 = QPixmap(os.path.join(path,"asset/C_yes.png"))
    self.ui.imageLabel_28.setPixmap(pix_28.scaled(w,h,Qt.KeepAspectRatio))

    pix_29 = QPixmap(os.path.join(path,"asset/C_no.png"))
    self.ui.imageLabel_29.setPixmap(pix_29.scaled(w,h,Qt.KeepAspectRatio))

    pix_30 = QPixmap(os.path.join(path,"asset/Z_yes.png"))
    self.ui.imageLabel_30.setPixmap(pix_30.scaled(w,h,Qt.KeepAspectRatio))

    pix_31 = QPixmap(os.path.join(path,"asset/Z_no.png"))
    self.ui.imageLabel_31.setPixmap(pix_31.scaled(w,h,Qt.KeepAspectRatio))

    pix_32 = QPixmap(os.path.join(path,"asset/P_yes.png"))
    self.ui.imageLabel_32.setPixmap(pix_32.scaled(w,h,Qt.KeepAspectRatio))

    pix_33 = QPixmap(os.path.join(path,"asset/P_no.png"))
    self.ui.imageLabel_33.setPixmap(pix_33.scaled(w,h,Qt.KeepAspectRatio))

    pix_34 = QPixmap(os.path.join(path,"asset/OP_yes.png"))
    self.ui.imageLabel_34.setPixmap(pix_34.scaled(w,h,Qt.KeepAspectRatio))

    pix_35 = QPixmap(os.path.join(path,"asset/OP_no.png"))
    self.ui.imageLabel_35.setPixmap(pix_35.scaled(w,h,Qt.KeepAspectRatio))

    pix_36 = QPixmap(os.path.join(path,"asset/SAF_activated.png"))
    self.ui.imageLabel_36.setPixmap(pix_36.scaled(w,h,Qt.KeepAspectRatio))

    pix_37 = QPixmap(os.path.join(path,"asset/OD_PC.png"))
    self.ui.imageLabel_37.setPixmap(pix_37.scaled(w,h,Qt.KeepAspectRatio))

    pix_38 = QPixmap(os.path.join(path,"asset/specialPath.png"))
    self.ui.imageLabel_38.setPixmap(pix_38.scaled(w,h,Qt.KeepAspectRatio))

    pix_39 = QPixmap(os.path.join(path,"asset/killLPC.png"))
    self.ui.imageLabel_39.setPixmap(pix_39.scaled(w,h,Qt.KeepAspectRatio))

    pix_40 = QPixmap(os.path.join(path,"asset/R0_AS.png"))
    self.ui.imageLabel_40.setPixmap(pix_40.scaled(w,h,Qt.KeepAspectRatio))

    rect = QRect(QPoint(20,0),QSize(620,685))

    self.ui.imageLabel_Source.setGeometry(rect)
    self.ui.imageLabel.setGeometry(rect)
    self.ui.imageLabel_2.setGeometry(rect)
    self.ui.imageLabel_3.setGeometry(rect)
    self.ui.imageLabel_4.setGeometry(rect)
    self.ui.imageLabel_5.setGeometry(rect)
    self.ui.imageLabel_6.setGeometry(rect)
    self.ui.imageLabel_7.setGeometry(rect)
    self.ui.imageLabel_8.setGeometry(rect)
    self.ui.imageLabel_9.setGeometry(rect)
    self.ui.imageLabel_10.setGeometry(rect)
    self.ui.imageLabel_11.setGeometry(rect)
    self.ui.imageLabel_12.setGeometry(rect)
    self.ui.imageLabel_13.setGeometry(rect)
    self.ui.imageLabel_14.setGeometry(rect)
    self.ui.imageLabel_15.setGeometry(rect)
    self.ui.imageLabel_16.setGeometry(rect)
    self.ui.imageLabel_17.setGeometry(rect)
    self.ui.imageLabel_18.setGeometry(rect)
    self.ui.imageLabel_19.setGeometry(rect)
    self.ui.imageLabel_20.setGeometry(rect)
    self.ui.imageLabel_21.setGeometry(rect)
    self.ui.imageLabel_22.setGeometry(rect)
    self.ui.imageLabel_23.setGeometry(rect)
    self.ui.imageLabel_24.setGeometry(rect)
    # self.ui.imageLabel_25.setGeometry(rect)
    self.ui.imageLabel_26.setGeometry(rect)
    self.ui.imageLabel_27.setGeometry(rect)
    self.ui.imageLabel_28.setGeometry(rect)
    self.ui.imageLabel_29.setGeometry(rect)
    self.ui.imageLabel_30.setGeometry(rect)
    self.ui.imageLabel_31.setGeometry(rect)
    self.ui.imageLabel_32.setGeometry(rect)
    self.ui.imageLabel_33.setGeometry(rect)
    self.ui.imageLabel_34.setGeometry(rect)
    self.ui.imageLabel_35.setGeometry(rect)
    self.ui.imageLabel_36.setGeometry(rect)
    self.ui.imageLabel_37.setGeometry(rect)
    self.ui.imageLabel_38.setGeometry(rect)
    self.ui.imageLabel_39.setGeometry(rect)
    self.ui.imageLabel_40.setGeometry(rect)

    self.stack = self.ui.tableWidget_2
    self.stack.setRowCount(1)
    self.stack.setColumnCount(1)

    self.stack.verticalHeader().setVisible(False)

    headerx = QTableWidgetItem()
    headerx.setText("TOS")
    self.stack.setHorizontalHeaderItem(0,headerx)

    self.table= self.ui.tableWidget
    self.table.setRowCount(256)
    self.table.setColumnCount(2)
    self.table.verticalHeader().setVisible(False)

    header2 = QTableWidgetItem()
    header2.setText("Value")
    self.table.setHorizontalHeaderItem(1,header2)

    header1 = QTableWidgetItem()
    header1.setText("Address")
    self.table.setHorizontalHeaderItem(0,header1)

    rect2 = QRect(QPoint(0,0),QSize(self.width(),self.height()))
    self.ui.scrollArea.setWidget(self.ui.logBox)
    self.ui.PC_value.setText("0")
    self.ui.SP_value.setText("FF")
    self.ui.IR_value.setText("Opcode : XX")
    self.ui.OR_value.setText("XX")
    self.ui.Instruction_value.setText("Instruction : XX")
    self.ui.run10ClockCycle.setVisible(True)

  def on_nextStage_clicked(self):
    arch = self.inst_emulator.TraceVector[self.trace_index][0]
    march = self.inst_emulator.TraceVector[self.trace_index][1]

    controlBits = march.ControlBits
    print(controlBits)
    print("Click")
    PC = arch.PC
    SP = arch.SP
    OR = march.OperandRegister
    IR_reg = march.InstructionRegister
    flagArray = arch.Flags
    registerArray = arch.Registers
    memoryContents = arch.Memory
    state = march.State

    #Calculate from Regfile diff
    currentNew = -1

    # One Line of State has been read
    # if(controlBits[0] and (not controlBits[1]) and controlBits[2] and (not controlBits[3]) and (not controlBits[4]) and controlBits[5] and (not controlBits[6]) and (not controlBits[7]) and (not controlBits[8]) and (not controlBits[9]) and controlBits[10] and (not controlBits[11]) and (not controlBits[12]) and (not controlBits[13]) and (not controlBits[14]) and (not controlBits[15]) and (not controlBits[16]) and (not controlBits[17]) and (not controlBits[18]) and (not controlBits[19]) and (not controlBits[20]) and (not controlBits[21]))
    #     executionState = 0
        # 1 0 1 0
        # 0 1 0 0
        # 0 0 1 0
        # 0 0 0 0
        # 0 0 0 0
        # 0 0
    self.ui.state.setText(hex(state))
    self.ui.PC_value.setText(hex(PC))
    self.ui.SP_value.setText(hex((SP+256 - 1)%256))
    self.ui.OR_value.setText(hex(OR))
    self.ui.IR_value.setText("Opcode : "+hex(IR_reg))

    output = prettyPrintOpDecode(IR_reg)

    redColor = QPalette()
    redColor.setColor(QPalette.WindowText,Qt.red)

    blackColor = QPalette()
    blackColor.setColor(QPalette.WindowText,Qt.black)

    self.ui.Instruction_value.setText("Instruction : "+output)

    self.ui.R0_value.setPalette(blackColor)
    self.ui.R0_value.setText(hex(registerArray[0]))
    self.ui.R1_value.setPalette(blackColor)
    self.ui.R1_value.setText(hex(registerArray[1]))
    self.ui.R2_value.setPalette(blackColor)
    self.ui.R2_value.setText(hex(registerArray[2]))
    self.ui.R3_value.setPalette(blackColor)
    self.ui.R3_value.setText(hex(registerArray[3]))
    self.ui.R4_value.setPalette(blackColor)
    self.ui.R4_value.setText(hex(registerArray[4]))
    self.ui.R5_value.setPalette(blackColor)
    self.ui.R5_value.setText(hex(registerArray[5]))
    self.ui.R6_value.setPalette(blackColor)
    self.ui.R6_value.setText(hex(registerArray[6]))
    self.ui.R7_value.setPalette(blackColor)
    self.ui.R7_value.setText(hex(registerArray[7]))

    #     switch(currentNew){
    #     case 0:
    #         ui.R0_value.setPalette(redColor)
    #         break
    #     case 1:
    #         ui.R1_value.setPalette(redColor)
    #         break
    #     case 2:
    #         ui.R2_value.setPalette(redColor)
    #         break
    #     case 3:
    #         ui.R3_value.setPalette(redColor)
    #         break
    #     case 4:
    #         ui.R4_value.setPalette(redColor)
    #         break
    #     case 5:
    #         ui.R5_value.setPalette(redColor)
    #         break
    #     case 6:
    #         ui.R6_value.setPalette(redColor)
    #         break
    #     case 7:
    #         ui.R7_value.setPalette(redColor)
    #         break
    #     default:
    #         break
    #     }


    #     sprintf(tempString,"%X",flagArray[0])
    # //    ui.R0_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[1])
    # //    ui.R1_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[2])
    # //    ui.R2_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[3])
    # //    ui.R3_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[4])
    # //    ui.R4_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[5])
    # //    ui.R5_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[6])
    # //    ui.R6_value_2.setText(tempString)
    #     sprintf(tempString,"%X",flagArray[7])
    # //    ui.R7_value_2.setText(tempString)


    self.ui.imageLabel.setVisible(controlBits[0])
    self.ui.imageLabel_2.setVisible(controlBits[1])
    self.ui.imageLabel_3.setVisible(controlBits[2])
    self.ui.imageLabel_4.setVisible(controlBits[3])
    self.ui.imageLabel_5.setVisible(controlBits[4])
    self.ui.imageLabel_6.setVisible(controlBits[5])
    self.ui.imageLabel_7.setVisible(controlBits[6])
    self.ui.imageLabel_39.setVisible(controlBits[6])
    self.ui.imageLabel_8.setVisible(controlBits[7])
    self.ui.imageLabel_9.setVisible(controlBits[8])
    self.ui.imageLabel_10.setVisible(controlBits[9])
    self.ui.imageLabel_11.setVisible(controlBits[10])
    self.ui.imageLabel_12.setVisible(controlBits[11])
    self.ui.imageLabel_13.setVisible(controlBits[12])
    self.ui.imageLabel_14.setVisible(controlBits[13])
    self.ui.imageLabel_15.setVisible(controlBits[14])
    self.ui.imageLabel_16.setVisible(controlBits[15])
    self.ui.imageLabel_17.setVisible(controlBits[16])
    self.ui.imageLabel_18.setVisible(controlBits[17])
    self.ui.imageLabel_19.setVisible(controlBits[18])
    self.ui.imageLabel_20.setVisible(controlBits[19])
    self.ui.imageLabel_21.setVisible(controlBits[20])
    self.ui.imageLabel_22.setVisible(controlBits[21])
    self.ui.imageLabel_23.setVisible(controlBits[0] or controlBits[4] or controlBits[11] or controlBits[13] or controlBits[15] or controlBits[19] or controlBits[21])
    self.ui.imageLabel_24.setVisible(controlBits[8] and controlBits[9])
    self.ui.imageLabel_27.setVisible(controlBits[18])
    self.ui.imageLabel_26.setVisible(controlBits[20])
    self.ui.imageLabel_35.setVisible(controlBits[17])

    self.ui.imageLabel_28.setVisible(flagArray[2])
    self.ui.imageLabel_29.setVisible(flagArray[3])
    self.ui.imageLabel_30.setVisible(flagArray[0])
    self.ui.imageLabel_31.setVisible(flagArray[1])
    self.ui.imageLabel_32.setVisible(flagArray[4])
    self.ui.imageLabel_33.setVisible(flagArray[5])
    self.ui.imageLabel_34.setVisible(flagArray[6])
    self.ui.imageLabel_35.setVisible(flagArray[7])
    self.ui.imageLabel_38.setVisible(controlBits[5] and controlBits[6])
    # //    ui.imageLabel_37.setVisible(controlBits[5] and controlBits[6])

    self.ui.imageLabel_40.setVisible((not controlBits[3]) and (not controlBits[2]) and (controlBits[0] or controlBits[1]))
    if(controlBits[5] and controlBits[6]):
      self.ui.imageLabel_7.setVisible(False)

    self.ui.imageLabel_37.setVisible(controlBits[6] and controlBits[7])
    self.ui.imageLabel_36.setVisible(controlBits[17])
    if((controlBits[18] and controlBits[20]) or controlBits[17]):
      self.ui.imageLabel_19.setVisible(False)
      self.ui.imageLabel_21.setVisible(False)
    self.ui.OR_value.setVisible(False)
    self.ui.label_2.setVisible(False)

    if(controlBits[15] or controlBits[16] or controlBits[17] or (controlBits[5] and controlBits[6])):
      self.ui.OR_value.setVisible(True)
      self.ui.label_2.setVisible(True)
    
    for j in range(0,255):
      self.table.setItem(j, 0, QTableWidgetItem(hex(j)))
      self.table.setItem(j, 1, QTableWidgetItem(hex(memoryContents[j])))

    localTOS = (SP+256 - 1)%256
    heightOfStack = 255 - localTOS
    if(heightOfStack < 0):
      heightOfStack = 0

    self.stack.setColumnCount(1)
    self.stack.setRowCount(heightOfStack)
    for iterator in range(0,heightOfStack):
      self.stack.setItem(iterator, 0, QTableWidgetItem(hex(memoryContents[255-heightOfStack+iterator+1])))

    if(self.trace_index == 0):
      self.ui.Instruction_value.setText("Instruction : XX")
      self.ui.R0_value.setText("XX")
      self.ui.R1_value.setText("XX")
      self.ui.R2_value.setText("XX")
      self.ui.R3_value.setText("XX")
      self.ui.R4_value.setText("XX")
      self.ui.R5_value.setText("XX")
      self.ui.R6_value.setText("XX")
      self.ui.R7_value.setText("XX")

    self.trace_index = self.trace_index + 1
    self.inst_emulator.step_n(1)

  def on_pushButton_clicked(self):
    self.ui.logBox.setText("Compiling source files\n")
    try:
      self.last_compiled_mem,self.log_string = self.inst_assembler.compile(self.ui.plainTextEdit.toPlainText())
    except:
      print("Error")
      self.ui.logBox.setText("Syntax Error\n")
      return

    self.inst_emulator.end_emulation()
    # print("Reset")
    self.inst_emulator.load_memory(self.last_compiled_mem)
    self.inst_emulator.start()
    self.inst_emulator.step_n(1)
    self.trace_index = 0
    self.on_nextStage_clicked()
    # self.inst_emulator.step_n(10)

    # self.ui.pushButton.setEnabled(False)
    # self.ui.pushButton_2.setEnabled(False)
    # self.ui.reset.setEnabled(False)
    # self.ui.nextStage.setEnabled(False)
    self.ui.logBox.setText(self.log_string)


    # self.on_reset_clicked()
    # self.ui.pushButton.setEnabled(True)
    # self.ui.pushButton_2.setEnabled(True)
    # self.ui.reset.setEnabled(True)
    # self.ui.nextStage.setEnabled(True)

  def on_pushButton_2_clicked(self):
    self.ui.logBox.setText(self.log_string)

  def on_reset_clicked(self):
    self.inst_emulator.end_emulation()
    # print("Reset")
    self.inst_emulator.load_memory(self.last_compiled_mem)
    self.inst_emulator.start()
    self.inst_emulator.step_n(1)
    self.trace_index = 0
    self.on_nextStage_clicked()

  def on_run10ClockCycle_clicked(self):
    for i in range(10):
      self.on_nextStage_clicked()
#### End of GUI Section
