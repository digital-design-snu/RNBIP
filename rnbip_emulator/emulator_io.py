import random
import pdb
import os
import datetime
import platform
import re
import sys
import tkinter as tk

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
