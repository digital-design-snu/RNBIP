import time
import logging
import random
import pdb
import os
import datetime;
import platform
import re
import sys

from RNBIP_ISA import *

def log(x):
  flag=0;
  if len(str(x)) ==1:
    x = '0'+str(x)
  if len(str(x)) == 2:
    if str(x)[0] in ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','0'] and str(x)[1] in ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','0'] :
      return x;
    return("Error @ "+" \""+str(x)+"\" is not a recognised Literal\n")
  return("Error @ "+" \""+str(x)+"\" is not a recognised Instruction\n")

class rnbip_assembler():
  
  @staticmethod
  def file_len(fname):
    i=0
    with fname as f:
      for i, l in enumerate(f):
        pass
    return i + 1
  
  @staticmethod
  def tobin(x):
    binary = ''
    if len(x) == 2:
      for i in x:
        # print(i)
        binary = binary+Hex2Bin_LUT(i.strip())
    elif len(x)==1:
      x="0"+x
    for i in x:
      binary = binary+Hex2Bin_LUT(i.strip())
    return binary

  def compile(self,str_asm):
    list_of_od_operations=["MVI R","ADI R","SBI R","ACI R","SCI R","ANI R","ORI R","XRI R","JUD","CUD","JCD R","CCD R","JCA R","CCA R","RTC R"]
    for codes in list_of_od_operations:
      if "R" == codes[len(codes)-1]:
        for i in range(0,8):
          list_of_od_operations.append(codes+str(i))
    list_of_flags = ["Z","NZ","C","NC","P","N","OP","EP"]
    #print(os.path.dirname(__file__))
    counter = 0;
    flag=1;
    labels = [];
    temp_str = ""
    log_str = ""
    out_str = ""
    final_binary = ""
    for line in str_asm.splitlines():
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
              tline = assembly2IR_LUT(line.strip())
              if(tline == "CHECK_LITERAL"):
                line = log(line.strip())
              else:
                line = tline
              if line.strip() in list_of_od_operations:
                line = line + "\n" + temp
              else:
                print("inside first else")
                line = log(line)+ "\n" + temp
        output = line.strip();
        # print(output);
        if len(output) < 20:
          temp_str = temp_str + output+"\n"
        else:
          print("inside log")
          log_str = log_str + "Error at " + output
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
            tline = assembly2IR_LUT(line.strip())
            if(tline == "CHECK_LITERAL"):
              line = log(line.strip())
            else:
              line = tline
            if line.strip() in list_of_od_operations:
              #print("inside od list")
              #print (line)
              line = line + "\n" + temp
            else:
              print("inside log else")
              line = log(line)+ "\n" + temp
      if len(line) < 20:
        #print(line)
        temp_str = temp_str + line +"\n"
      else:
        print("here")
        log_str = log_str + "Error at " + line
        sys.exit()
    # print("done")

    for line in temp_str.splitlines():
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
                toutput = assembly2IR_LUT(x[0]);
                if(toutput == "CHECK_LITERAL"):
                  output = log(x[0])
                else:
                  output = toutput
                # print(output);
                out_str = out_str + str(output)+"\n"
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
              tline = assembly2IR_LUT(line)
              if(tline == "CHECK_LITERAL"):
                line = log(line)
              else:
                line = tline
              if line.strip() in list_of_od_operations:
                line = line.upper() + "\n" + temp
              else:
                line = log(line.upper())+ "\n" + temp
              # line = line.upper() + "\n" + temp
          output = line.strip()
          # output = line[line.index(':')+1:].strip().upper();
          # print(output);
          if is_inside == 1:
            if len(output)<20:
              out_str = out_str + output+"\n"
            else:
              sys.exit()
              log_str = log_str + "Error at " + output
          else:
            toutput = assembly2IR_LUT(line.strip().upper())
            if(toutput == "CHECK_LITERAL"):
              output = log(line.strip().upper())
            else:
              output = toutput
            if len(output)<20:
              out_str = out_str + output+"\n"
            else:
              sys.exit()
              log_str = log_str + "Error at " + output
      else:
        if len(labels)!=0:
            for x in labels:
              if x[1] == line.strip():
                # print(x[0])
                toutput = assembly2IR_LUT(x[0]);
                if(toutput == "CHECK_LITERAL"):
                  output = log(x[0])
                else:
                  output = toutput
                # print(output);
                out_str = out_str + str(output)+"\n"
                lab=1;
                break
        if lab==0:
          is_inside = 0;
          if " " in line.strip():
            if len([m.start() for m in re.finditer(r" ",line)]) > 1:
              # print("if")
              # print(line)
              is_inside = 1;
              temp = line[[m.start() for m in re.finditer(r" ",line)][1]:]
              if temp.strip() in list_of_flags:
                temp = "0"+str(list_of_flags.index(temp.strip()))
              line = line[0:[m.start() for m in re.finditer(r" ",line)][1]]
              tline = assembly2IR_LUT(line)
              if(tline == "CHECK_LITERAL"):
                line = log(line)
              else:
                line = tline
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
              out_str = out_str + output+"\n"
            else:
              log_str = log_str + "Error at " + output
              sys.exit()
          else:
            #print("this is where it should be:"+line)
            tempx = 0
            output = IR2Binary_LUT(line.strip().upper())
            # print(output)
            if output.isdigit():
              tempx=1
            try:
              int(output, 16)
              tempx = 1
            except ValueError:
              tempx = 0
            if len(output)<20 and tempx==1 :
              out_str = out_str + output+"\n"
            else:
              print("lof 2")
              log_str = log_str + "Error at " + output
              sys.exit()
    if flag == 1:
      #print(str(datetime.datetime.now()));
      log_str = log_str + str(datetime.datetime.now()) + " Compilation Successful...\n"

    #2ND Pass
    #ControlFile = open("cc.txt","w")
    for line in out_str.splitlines() :
      if "//" not in line.strip():
        output = IR2Binary_LUT(line.strip());
        # print(output);
        if output.strip() != "":
          try:
            int(output.strip(),16)
            if len(output) <= 2:
              output = bin(int(output.strip(),16))[2:].zfill(8)

            #print "this is the output: "+output
          except ValueError:
            output = output.strip()

          final_binary = final_binary + output+"\n"
    # print(final_binary)
    num_lines = len(final_binary.splitlines())
    # Add Segmentation and Partial Flash modes
    while num_lines<=255:
      final_binary = final_binary + "00000000"+"\n"
      num_lines+=1
    return final_binary,log_str
    # outFile = open("memory.bin","w")
    # outFile.write(final_binary)