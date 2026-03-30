import random
import datetime

# Global List Declaration 
name = []
phno = []
add = []
checkin = []
checkout = []
room = []
price = []
rc = []
p = []
roomno = []
custid = []
day = []

# Global Variable Declaration

i = 0

# Home Function
def Home():
	
	print("WELCOME TO HOTEL AG\n")
	print("1 Booking\n")
	print("2 Rooms Info\n")
	print("3 Room Service(Menu Card)\n")
	print("4 Payment\n")
	print("5 Record\n")
	print("0 Exit\n")

	ch=int(input("->"))
	
	if ch == 1:
		print(" ")
		Booking()
	
	elif ch == 2:
		print(" ")
		Rooms_Info()
	
	elif ch == 3:
		print(" ")
		restaurant()
	
	elif ch == 4:
		print(" ")
		Payment()
	
	elif ch == 5:
		print(" ")
		Record()
	
	else:
		exit()

# Function used in booking

def date(c):
	
	if c[2] >= 2020 and c[2] <= 2025:
		
		if c[1] != 0 and c[1] <= 12:
			
			if c[1] == 2 and c[0] != 0 and c[0] <= 31:
				
				if c[2]%4 == 0 and c[0] <= 29:
					pass
				
				elif c[0]<29:
					pass
				
				else:
					print("Invalid date\n")
					name.pop(i)
					phno.pop(i)
					add.pop(i)
					checkin.pop(i)
					checkout.pop(i)
					Booking()
			
			
			# if month is odd & less than equal 
			# to 7th month 
			elif c[1] <= 7 and c[1]%2 != 0 and c[0] <= 31:
				pass
			
			# if month is even & less than equal to 7th
			# month and not 2nd month
			elif c[1] <= 7 and c[1]%2 == 0 and c[0] <= 30 and c[1] != 2:
				pass
			
			# if month is even & greater than equal 
			# to 8th month
			elif c[1] >= 8 and c[1]%2 == 0 and c[0] <= 31:
				pass
			
			# if month is odd & greater than equal
			# to 8th month
			elif c[1]>=8 and c[1]%2!=0 and c[0]<=30: 
				pass
			
			else: 
				print("Invalid date\n")
				name.pop(i)
				phno.pop(i)
				add.pop(i)
				checkin.pop(i)
				checkout.pop(i)
				Booking()
				
		else:
			print("Invalid date\n")
			name.pop(i)
			phno.pop(i)
			add.pop(i)
			checkin.pop(i)
			checkout.pop(i)
			Booking()
			
	else:
		print("Invalid date\n")
		name.pop(i)
		phno.pop(i)
		add.pop(i)
		checkin.pop(i)
		checkout.pop(i)
		Booking()


# Booking function 
def Booking():
	
		# used global keyword to 
		# use global variable 'i'
		global i
		print(" BOOKING ROOMS")
		print(" ")
		
		while 1:
			n = str(input("Name: "))
			p1 = str(input("Phone No.: "))
			a = str(input("Address: "))
			
			# checks if any field is not empty
			if n!="" and p1!="" and a!="":
				name.append(n)
				add.append(a)
				break
				
			else:
				print("\tName, Phone no. & Address cannot be empty..!!")
			
		cii=str(input("Check-In: "))
		checkin.append(cii)
		cii=cii.split('/')
		ci=cii
		ci[0]=int(ci[0])
		ci[1]=int(ci[1])
		ci[2]=int(ci[2])
		date(ci)
		
		coo=str(input("Check-Out: "))
		checkout.append(coo)
		coo=coo.split('/')
		co=coo
		co[0]=int(co[0])
		co[1]=int(co[1])
		co[2]=int(co[2])
		
		# checks if check-out date falls after 
		# check-in date
		if co[1]<ci[1] and co[2]<ci[2]:
			
			print("\n\tErr..!!\n\tCheck-Out date must fall after Check-In\n")
			name.pop(i)
			add.pop(i)
			checkin.pop(i)
			checkout.pop(i)
			Booking()
		elif co[1]==ci[1] and co[2]>=ci[2] and co[0]<=ci[0]:
			
			print("\n\tErr..!!\n\tCheck-Out date must fall after Check-In\n")
			name.pop(i)
			add.pop(i)
			checkin.pop(i)
			checkout.pop(i)
			Booking()
		else:
			pass
		
		date(co)
		d1 = datetime.datetime(ci[2],ci[1],ci[0])
		d2 = datetime.datetime(co[2],co[1],co[0])
		d = (d2-d1).days
		day.append(d)
		
		print("----SELECT ROOM TYPE----")
		print(" 1. Standard Non-AC")
		print(" 2. Standard AC")
		print(" 3. 3-Bed Non-AC")
		print(" 4. 3-Bed AC")
		print(("\t\tPress 0 for Room Prices"))
		
		ch=int(input("->"))
		
		# if-conditions to display allotted room
		# type and it's price
		if ch==0:
			print(" 1. Standard Non-AC - Rs. 1000")
			print(" 2. Standard AC - Rs. 5000")
			print(" 3. 3-Bed Non-AC - Rs. 7000")
			print(" 4. 3-Bed AC - Rs. 10000")
			ch=int(input("->"))
		if ch==1:
			room.append('Standard Non-AC')
			print("Room Type- Standard Non-AC") 
			price.append(5000)
			print("Price- 5000")
		elif ch==2:
			room.append('Standard AC')
			print("Room Type- Standard AC")
			price.append(8000)
			print("Price- 8000")
		elif ch==3:
			room.append('3-Bed Non-AC')
			print("Room Type- 3-Bed Non-AC")
			price.append(11000)
			print("Price- 11000")
		elif ch==4:
			room.append('3-Bed AC')
			print("Room Type- 3-Bed AC")
			price.append(14000)
			print("Price- 14000")
		else:
			print(" Wrong choice..!!")


		# randomly generating room no. and customer 
		# id for customer
		rn = random.randrange(40)+300
		cid = random.randrange(100)+100
		
		
		# checks if allotted room no. & customer 
		# id already not allotted
		while rn in roomno or cid in custid:
			rn = random.randrange(60)+300
			cid = random.randrange(60)+100
			
		rc.append(0)
		p.append(0)
			
		if p1 not in phno:
			phno.append(p1)
		elif p1 in phno:
			for n in range(0,i):
				if p1== phno[n]:
					if p[n]==1:
						phno.append(p1)
		elif p1 in phno:
			for n in range(0,i):
				if p1== phno[n]:
					if p[n]==0:
						print("\tPhone no. already exists and payment yet not done..!!")
						name.pop(i)
						add.pop(i)
						checkin.pop(i)
						checkout.pop(i)
						Booking()
		print("")
		print("***ROOM BOOKED SUCCESSFULLY***\n")
		print("Room No. - ",rn)
		print("Customer Id - ",cid)
		roomno.append(rn)
		custid.append(cid)
		i=i+1
		n=int(input("0-BACK\n ->"))
		if n==0:
			Home()
		else:
			exit()

# ROOMS INFO 
def Rooms_Info():
	print("HOTEL ROOMS INFO ")
	print("")
	print("STANDARD NON-AC")
	print("------------------------------------------------------------------------------------")
	print("Room amenities include: 1 Double Bed, Television, Telephone,")
	print("Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and")
	print("an attached washroom with hot/cold water.\n")
	print("STANDARD NON-AC")
	print("------------------------------------------------------------------------------------")
	print("Room amenities include: 1 Double Bed, Television, Telephone,")
	print("Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and")
	print("an attached washroom with hot/cold water + Window/Split AC.\n")
	print("3-Bed NON-AC")
	print("---------------------------------------------------------------------------------------")
	print("Room amenities include: 1 Double Bed + 1 Single Bed, Television,")
	print("Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, 1")
	print("Side table, Balcony with an Accent table with 2 Chair and an")
	print("attached washroom with hot/cold water.\n")
	print("3-Bed AC")
	print("----------------------------------------------------------------------------------------")
	print("Room amenities include: 1 Double Bed + 1 Single Bed, Television,")
	print("Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, ")
	print("1 Side table, Balcony with an Accent table with 2 Chair and an")
	print("attached washroom with hot/cold water + Window/Split AC.\n\n")
	print("-------------------------------------------------------------------------------------------")
	print()
	n=int(input("0-BACK\n ->"))
	if n==0:
		Home()
	else:
		exit()

# RESTAURANT FUNCTION 
def restaurant():
	ph=int(input("Customer Id: "))
	global i
	f=0
	r=0
	for n in range(0,i):
		if custid[n]==ph and p[n]==0:
			f=1
			print("-------------------------------------------------------------------------")
			print("                            Hotel AG        ")
			print("-------------------------------------------------------------------------")
			print("                            Menu Card")
			print("-------------------------------------------------------------------------")
			print("\n---------BEVARAGES--------- 	                        ")
			print("--------------------------------------------")
			print(" 1 Regular Tea........................80.00        26 Dal Fry....................200.00")
			print(" 2 Masala Tea.........................90.00        27 Dal Makhani...........220.00")
			print(" 3 Coffee..................................90.00   28 Dal Tadka................230.00")
			print(" 4 Drinks ..........................140.00          -----------ROTI------------")
			print(" 5 Bread Butter.......................90.00        29 Plain Roti.............. 20.00")
			print(" 6 Bread Jam..........................80.00        30 Butter Roti............. 25.00")
			print(" 7 Veg. Sandwich....................120.00         31 Tandoori Roti........... 30.00")
			print(" 8 Veg. Toast Sandwich.........130.00              32 Butter Naan............. 40.00")
			print(" 9 Cheese Toast Sandwich... 160.00")
			print(" 10 Grilled Sandwich............150.00") 
			print("----------SOUPS------------------------------------------------RICE----------")
			print("		                                         33 Plain Rice.............. 70.00")
			print("----------------------------------	         34 Jeera Rice.............. 90.00")
			print("11 Tomato Soup...............110.00               35 Veg Pulao.............. 100.00")
			print("12 Hot & Sour..................110.00             36 Peas Pulao............. 110.00")
			print("13 Veg. Noodle Soup........110.00")
			print(" 14 Sweet Corn.................110.00          ----------SOUTH INDIAN----------")
			print(" 15 Veg. Munchow............110.00")
			print("                                                  37 Plain Dosa.................60.00")
			print(" ----------MAIN COURSE----------		         38 Onion Dosa...............70.00")
			print("----------------------------------	         39 Masala Dosa.............70.00")
			print(" 16 Shahi Paneer.............450.00               40 Paneer Dosa..............90.00")
			print(" 17 Kadai Paneer............400.00	         41 Rice Idli.....................40.00")
			print(" 18 Handi Paneer............500.00                42 Sambhar Vada...........30.00")
			print(" 19 Palak Paneer............400.00")
			print(" 20 Chilli Paneer............440.00            -----------ICE CREAM----------")
			print(" 21 Matar Mushroom....400.00	 ")
			print(" 22 Mix Veg................... 350.00	        43 Vanilla................. 60.00")
			print(" 23 Jeera Aloo................300.00	        44 Strawberry.............. 80.00")
			print(" 24 Malai Kofta..............300.00	        45 Pineapple............... 70.00")
			print(" 25 Aloo Matar...............250.00	        46 Butter Scotch........... 90.00")
			print("Press 0 -to end ")
			ch=1
			while(ch!=0):
				
				ch=int(input(" -> "))
				
				# if-elif-conditions to assign item
				# prices listed in menu card
				if ch==1 or ch==31 or ch==32:
					rs=20
					r=r+rs
				elif ch<=4 and ch>=2:
					rs=25
					r=r+rs
				elif ch<=6 and ch>=5:
					rs=30
					r=r+rs
				elif ch<=8 and ch>=7:
					rs=50
					r=r+rs
				elif ch<=10 and ch>=9:
					rs=70
					r=r+rs
				elif (ch<=17 and ch>=11) or ch==35 or ch==36 or ch==38:
					rs=110
					r=r+rs
				elif ch<=19 and ch>=18:
					rs=120
					r=r+rs
				elif (ch<=26 and ch>=20) or ch==42:
					rs=140
					r=r+rs
				elif ch<=28 and ch>=27:
					rs=150
					r=r+rs
				elif ch<=30 and ch>=29:
					rs=15
					r=r+rs
				elif ch==33 or ch==34:
					rs=90
					r=r+rs
				elif ch==37:
					rs=100
					r=r+rs
				elif ch<=41 and ch>=39:
					rs=130
					r=r+rs
				elif ch<=46 and ch>=43:
					rs=60
					r=r+rs
				elif ch==0:
					pass
				else:
					print("Wrong Choice..!!")
			print("Total Bill: ",r)
			
			# updates restaurant charges and then 
			# appends in 'rc' list
			r=r+rc.pop(n)
			rc.append(r) 
		else:
			pass
	if f == 0:
		print("Invalid Customer Id")
	n=int(input("0-BACK\n ->"))
	if n==0:
		Home()
	else:
		exit()
	
				
# PAYMENT FUNCTION			 
def Payment():
	
	ph=str(input("Phone Number: "))
	global i
	f=0
	
	for n in range(0,i):
		if ph==phno[n] :
			
			# checks if payment is
			# not already done
			if p[n]==0:
				f=1
				print(" Payment")
				print(" --------------------------------")
				print(" MODE OF PAYMENT")
				
				print(" 1- Credit/Debit Card")
				print(" 2- Paytm/PhonePe")
				print(" 3- Using UPI")
				print(" 4- Cash")
				x=int(input("-> "))
				print("\n Amount: ",(price[n]*day[n])+rc[n])
				print(name)
				print(" (y/n)")
				ch=str(input("->"))
				
				if ch=='y' or ch=='Y':
					print("\n\n --------------------------------")
					print("---------------Hotel AG--------------")
					print(" ------------------------------------")
					print("--------------- Bill-----------------")
					print(" ------------------------------------")
					print(" Name: ",name[n],"\t\n Phone No.: ",phno[n],"\t\n Address: ",add[n],"\t")
					print("\n Check-In: ",checkin[n],"\t\n Check-Out: ",checkout[n],"\t")
					print("\n Room Type: ",room[n],"\t\n Room Charges: ",price[n]*day[n],"\t")
					print(" Restaurant Charges: \t",rc[n])
					print(" ------------------------------------")
					print("\n Total Amount: ",(price[n]*day[n])+rc[n],"\t")
					print(" ------------------------------------")
					print("--------------Thank You--------------")
					print(" ------------Visit Again :)----------")
					print(" --------------------------------\n")
					p.pop(n)
					p.insert(n,1)
					
					# pops room no. and customer id from list and 
					# later assigns zero at same position
					roomno.pop(n)
					custid.pop(n)
					roomno.insert(n,0)
					custid.insert(n,0)
					
			else:
				
				for j in range(n+1,i):
					if ph==phno[j] :
						if p[j]==0:
							pass
						
						else:
							f=1
							print("\n\tPayment has been Made :)\n\n") 
	if f==0: 
		print("Invalid Customer Id")
		
	n = int(input("0-BACK\n ->"))
	if n == 0:
		Home()
	else:
		exit()

# RECORD FUNCTION 
def Record():
	
	# checks if any record exists or not
	if phno!=[]:
		print("	 *** HOTEL RECORD ***\n")
		print("| Name	 | Phone No. | Address	 | Check-In | Check-Out	 | Room Type	 | Price	 |")
		print("----------------------------------------------------------------------------------------------------------------------")
		
		for n in range(0,i):
			print("|",name[n],"\t |",phno[n],"\t|",add[n],"\t|",checkin[n],"\t|",checkout[n],"\t|",room[n],"\t|",price[n])
		
		print("----------------------------------------------------------------------------------------------------------------------")
	
	else:
		print("No Records Found")
	n = int(input("0-BACK\n ->"))
	if n == 0:
		Home()
		
	else:
		exit()

# Driver Code 
Home()
