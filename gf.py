# A function to check whether the given inputs are valid or not.
# A valid A(x) and B(x) must have coefficients that are less than 2^(degree of P)
def checkinputs(A,B,P):
	M=A+B
	maxval = 2**(len(P)-1)
	isValid = 1
	if(len(A)>32):
		print "\nToo many terms for A , (max 32)\n"
		isValid = 0	

	if(len(B)>32):
		print "\nToo many terms for B , (max 32)\n"
		isValid = 0	

	for i in range(0,len(M)):
		if(M[i]>=maxval):
			isValid =0
			break

	if(not isValid):
		print "\n"
		print "Maximum value in (A,B) is",maxval-1,"for the given P(x) = "+' '.join(str(x) for x in P)	
		print "\n"



	return isValid


def removeZeros(A):
	while(A[0]==0 and len(A)>1):
		del(A[0])

# Converts a given integer n to its decimal equivalent. 
# m is the number of bits of n in binary form
# arr will be the array containing the binary equivalent of n.
# Example: n = 5; m = 3; arr = ['1','0','1'] 
def decToBin(n,m):
	q = n
	arr = range(m)
	counter = m-1
	while(counter>=0):
		arr[counter] = q % 2
		q =q/2
		counter -=1
	return arr	


# Performs bitwise XOR/modulo 2 addition given two binary numbers reprenseted as arrays of 1's and 0's
def bitXOR(bin1,bin2):
	pointer1 = len(bin1)-1
	pointer2 = len(bin2)-1
	result=[]
	while (pointer1 >= 0 and pointer2 >= 0):
		result.insert(0, bin1[pointer1]^bin2[pointer2])
		pointer1-=1
		pointer2-=1

	if(len(bin1)>len(bin2)):	# copy bin1's remaining contents
		while (pointer1>=0):
			result.insert(0,bin1[pointer1])
			pointer1-=1
	elif(len(bin1)<len(bin2)):		
		while (pointer2>=0):
			result.insert(0,bin2[pointer2])
			pointer2-=1

	return result
	
# Converts a given binary, in array form, to its equivalent decimal
# m is the number of bits of the binary number
def binToDec(bin,m):
	dec = 0
	expo = len(bin)-1
	for i in range(0,len(bin)):
		dec+=bin[i]*(2**expo)
		expo-=1
	return dec			


# galoisAdd performs both Addition and Subtraction (since these two operation are the same in Galois Fields)
# this function accepts two polynomials A and B in "1 0 4 3" form meaning x^3+4x+3 and m which is number of bits in the binary representation of the elements of GF(2^m)
def galoisAdd(A,B,m,display=0,op="+"):
	result = []

	if(len(A)<len(B)):	# B is larger. Swap them
		C = A
		A = B
		B = C

	pointerA = len(A)-1
	pointerB = len(B)-1

	if(display):
		print ' '*(6)+' '.join(str(x) for x in A)
		print ' '*(5)+op+' '*((len(A)-len(B))*2)+' '.join(str(x) for x in B)
		print ' '*(5)+"-"*(2*(len(A)+1))

	while (pointerA >= 0 and pointerB >= 0):
		result.insert(0,binToDec(bitXOR(decToBin(A[pointerA],m),decToBin(B[pointerB],m)),m))
		pointerA-=1
		pointerB-=1

	if(pointerA>pointerB):	# copy A's remaining contents
		while (pointerA>=0):
			result.insert(0,A[pointerA])
			pointerA-=1
	
	
	if(display):
		print ' '*(6+len(A)-len(result))+' '.join(str(x) for x in result)
		print "\n"+"*"*(len(result)*5 + 20)
		print "    ANSWER: A(x)"+op+"B(x) = "+'  '.join(str(x) for x in result)	
	return result		

# Performs bitwise multiplication given two binary numbers reprenseted as arrays of 1's and 0's
def bitMult(bin1,bin2,m):
	result = []
	r = []
	padding = [0]*m
	for i in range(0,m):
		padding.pop()
		if(bin2[i]):
			r = bin1 + padding
		else:
			r = [0]*m + padding
		result = bitXOR(result ,r)
	removeZeros(result)	
	return result

# Performs bitwise division given two binary numbers reprenseted as arrays of 1's and 0's
def bitDiv(smallBin,bigBin):
	rem = [] + bigBin
	while (len(rem)>len(smallBin)-1):
		rem = bitXOR(rem,smallBin + [0]*(len(rem)-len(smallBin)))
		removeZeros(rem)
	return rem


# Performs multiplication in Galois Fields  between 2 polynomials: A(x) and B(x) using 1 irreducible polynomial: P(x)
def galoisMult(A,B,P,m,display=0):
	result = []
	larger = A
	smaller = B
	if(len(B)>len(A)):
		larger = B
		smaller = A
	padding = []

	if(display):
		print ' '*3+ ' '*(len(larger)+len(smaller)+1)+' '.join(str(x) for x in larger)
		print ' '*4 + '*'+' '*((len(larger)+len(smaller)+1)+(len(larger)-len(smaller))*2-2)+' '.join(str(x) for x in smaller)
		print ' '*(4)+"-"*(2*(len(A)+len(B))+5)

	i = len(smaller) -1
	while i >=0:
		if(smaller[i] != 0):
			j = len(larger)-1
			temp = []
			while j >= 0:
				prod = bitMult(decToBin(smaller[i],m),decToBin(larger[j],m),m)
				if(len(prod) >m):	# Must be reduced using P(x)
					prod = bitDiv(P,prod)
				j-=1	
				temp.insert(0,binToDec(prod,m))
			
			temp += padding	
			if(display):
				print ' '*3+ ' '*(len(larger)+len(smaller)+1 - 2*(len(smaller) - i -1)) +' '.join(str(x) for x in temp)
			result = galoisAdd(temp ,result,m)	
		i-=1
		padding.append(0)
	if(display):	
		print ' '*(4)+"-"*(2*(len(A)+len(B)))
		print " "*(2+(len(larger)+len(smaller)-len(temp))*2)+' '.join(str(x) for x in result)
		print "\n"+"*"*(len(result)*5 + 20)
		print "    ANSWER: A(x)*B(x) = "+'  '.join(str(x) for x in result)	
	return result


# Performs division in Galois Fields between 2 polynomials: A(x) and B(x) using 1 irreducible polynomial: P(x)
def galoisDiv(A,B,P,m):
	rem = [] + A
	quotient = []
	prevlen = len(rem)
	while (len(rem)>len(B)-1):
		factor = 1
		desiredProd = rem[0]
		if(desiredProd != B[0]):
			factor= 2
			while (factor < 2**m ):
				potential = galoisMult([B[0]],[factor],P,m,0)
				if(potential[0] == desiredProd):
					break
				factor+=1

		quotient.append(factor)	

		temp = galoisMult(B,[factor],P,m) + [0]*(len(rem)-len(B)) 

			

		print ' '*(5+(len(A)-len(rem))*2) +' '.join(str(x) for x in rem)
		print ' '*(5+(len(A)-len(rem))*2) +' '.join(str(x) for x in temp)," =  B * ",factor," x^",(len(rem)-len(B))

		rem = galoisAdd(rem , temp,m)
		removeZeros(rem)
		print ' '*(5+(len(A)-len(rem))*2)  + "-"*(len(temp)*2+5)

		if(len(rem)<len(B)-1):
			quotient += [0]*(prevlen - len(B))	
		else:	
			quotient += [0]*(prevlen - len(rem)-1)	

		prevlen = len(rem)

	print ' '*(5+(len(A)-len(rem))*2) +'  '.join(str(x) for x in rem)," <- Remainder"
	if(len(quotient) == 0):
		quotient = [0]

	print "\n"+"*"*(len(quotient)*5 + 20)
	print "    ANSWER: A(x)/B(x) = "+'  '.join(str(x) for x in quotient)	
	return quotient




print "\n		( Galois Field Caluculator )"
print "....................................... (enter 'q' to Quit)\n"
while (True):
	
	while (True):	
		A = raw_input("Enter a polynomial A(x): ")
		if(A.lower()=='q'):
			exit()
		try:
			A = map(int,A.split())
			break
		except ValueError:
			print "\nThat is not a valid format for input A(x). Please enter again...\n"

	while (True):
		B = raw_input("Enter a polynomial B(x): ")
		if(B.lower()=='q'):
			exit()
		try:
			B = map(int,B.split())
			break
		except ValueError:
			print "\nThat is not a valid format for input B(x). Please enter again...\n"

	while (True):
		P = raw_input("Enter a polynomial P(x): ")
		if(P.lower()=='q'):
			exit()
		try:
			P = map(int,P.split())
			break
		except ValueError:
			print "\nThat is not a valid format for input P(x). Please enter again...\n"

	# Remove unnecessary 0's in from of the given polynomial if there are any
	removeZeros(A)
	removeZeros(B)
	removeZeros(P)

	if(checkinputs(A,B,P)):

		m = len(P)-1

		while(True):
			print "\n	Options: \n"+"	1. A(x) + B(x)\n	2. A(x) - B(x)\n	3. A(x) * B(x)\n	4. A(x) / B(x)\n	5. Change set of polynomials\n"
			op = raw_input("Choice: ")
			print '-'*60+"\n"
			if(op.lower()=='q'):
				exit()
			else:	
				op = int(op)
				if(op>0 and op<5):
					print "    GIVEN:	\n"
					print ' '*(5)+"A(x) = "+' '.join(str(x) for x in A)
					print ' '*(5)+"B(x) = "+' '.join(str(x) for x in B)
					if(op == 3 or op ==4):
						print ' '*(5)+"P(x) = "+' '.join(str(x) for x in P)+"\n"
					else:
						print "\n"	
					print "    SOLUTION:	\n"
					if(op==1 or op==2):
						if(op==2):
							galoisAdd(A,B,m,1,"-")
						else:
							galoisAdd(A,B,m,1)
						
					elif(op==3):
						galoisMult(A,B,P,m,1)
						
					elif(op==4):
						
						galoisDiv(A,B,P,m)
					print '-'*60
				
				elif(op==5):
					break

				else:
					print "Please enter a valid option"	

	