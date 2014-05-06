import sys
import regex as re
import os
f= open("input.txt",'rw+')
f1=open(“output.txt”,'a')
number=raw_input("How many pattern: ")
number=int(number)
new_char = []
miss=[]
check=""
desc_next=""
input_dist1=[]
input_dist2=[]
prod=1
"""-----------------Taking-Input-Parameters-and-Patterns--------------"""
for j in range(0,number):	
	new_char.append("(")
	input_var = raw_input("Enter pattern: ")
	input_var = list(input_var)
	for i in range(0,len(input_var)):
		if ((input_var[i].isalpha() and input_var[i] !="X") or input_var[i]=="[" or input_var[i]=="]"):
			new_char[j]=new_char[j]+input_var[i]
		elif input_var[i].isdigit():
			new_char[j]=new_char[j]+"{"+input_var[i]+"}"
		elif (input_var[i] == "X"):
			new_char[j]=new_char[j]+"."
		elif (input_var[i] == "{"):
			new_char[j]=new_char[j]+"[^"
		elif (input_var[i] == "}"):
			new_char[j]=new_char[j]+"]"
		else : 
			print "Error"
			sys.exit()
	new_char[j]=new_char[j]+")"	
	mis = raw_input("Mismatches Allowed: ")
	miss.append(mis)
	if(j==0):
		prod=(int(miss[0])+1)
	else:
		prod=prod*(int(miss[j])+1)
	if(j!=number-1):
		dist1 = raw_input("Enter lower position: ")
		input_dist1.append(int(dist1))
		dist2 = raw_input("Enter upper position: ")
		input_dist2.append(int(dist2))
"""--------------------Building-All-Combination-Errors----------------"""
l=[]
for i in range(0,number):
	count=0
	x=0
	while(count!=prod):		
		l.append("")
		l[count]=l[count]+str(x)+" "
		count=count+1
count=1
lst=""
while(count<prod):
	lst1 = l[count].split()
	for i in xrange(number-1,-1,-1):
		if(int(lst1[i])<int(miss[i])):
			lst1[i]=str(int(lst1[i])+1)
			l[count]=" ".join(lst1)			
			if (count<prod):
				l[count+1]=" ".join(lst1)
			count=count+1
			break
		else:
			lst1[i]=str(0)
count=0
files=[]
protein=""
lines=[]
lines=f.readlines()
lines.append(">")
"""-------------------------------Search-using-Regex------------------"""
while(count!=prod):
	new_char1=""	
	sum1=0
	lst1 = l[count].split()	
	j=0
	for j in range(0,number):
		if ((int(lst1[j])-1)<0):
			new_char1=new_char1+new_char[j]+"{s<"+str(int(lst1[j])+1)+",i<"+str(int(lst1[j])+1)+",d<"+str(int(lst1[j])+1)+"}"
		else:	
			new_char1=new_char1+new_char[j]+"{"+str(int(lst1[j])-1)+"<s<"+str(int(lst1[j])+1)+","+str(int(lst1[j])-1)+"<i<"+str(int(lst1[j])+1)+","+str(int(lst1[j])-1)+"<d<"+str(int(lst1[j])+1)+"}"
		if (j<number-1 and (input_dist1[j]!=0 or input_dist2[j]!=0)):
			new_char1=new_char1+"(\w){"+str(input_dist1[j])+","+str(input_dist2[j])+"}"
	protein=""
	check=0
	pos1=0
	desc_check=""	
	for row in lines:	
		if (ord(row[0])==10 or ord(row[0])==32):
			continue
		elif (ord(row[0])>64 and (ord(row[0])<92) and desc_next!=""):
			protein=protein+row
			continue	
		elif (ord(row[0])==62 and protein==""):
			desc_next=row
			pos1=check
			continue
		elif (ord(row[0])==62 and protein!=""):
			protein = protein.replace ('\n', '')			
			my_regex = re.compile(new_char1)	
			a = my_regex.findall(protein)
			if a:				
				for k in range(0,number):
					lst1[k]=int(lst1[k])
				sum1=sum(lst1)
				temp='temp'+str(sum1)+'.txt'
				files.append(sum(lst1))
				f2=open(temp,'a')
				f2.write(desc_check)
				f2.write(protein)
				f2.write("\n")			
				f2.close()
				lines[check]="$ "+lines[check]
			pos1=check			
			protein=""
			desc_check=row
		check=check+1				
	count=count+1
		
"""-------------------Storing-in-main-file----------------------------"""
if (files==[]):
	sys.exit()
else:
	for j in range(0,max(files)+1):
		temp='temp'+str(j)+'.txt'
		f2=open(temp,'a+')
		heading = "$ "+str(j)
		print >>f1, heading	
		for row in f2.readlines():		
			print >>f1, row
		f2.close()
		os.remove(temp)		
	f1.close()
	f.close()

