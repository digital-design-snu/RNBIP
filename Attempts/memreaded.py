i=0
a = []
f = open('machCode.bin')
while(i<256):
	line = f.readline()
	a.append(int(line,2))
	i = i+1
i=0
while(i<256):
	print(a[i])
	i = i+1
	
	
	
