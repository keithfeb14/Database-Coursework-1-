import sqlite3
import pandas as pd

#Creating the database
conn = sqlite3.connect('database')

#cursor to interact with the database
c = conn.cursor() 

########## Tables #######################

#Creating pilots table
c.execute("""CREATE TABLE IF NOT EXISTS Pilots (
  Pilot_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
  Name TEXT,
  Age INTEGER,
  Salary INTEGER
)""")

#Create aircrafts table
c.execute("""CREATE TABLE IF NOT EXISTS Aircrafts (
  Aircraft_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT,
  Capacity INTEGER
)""")

#Create flights table 
c.execute("""CREATE TABLE IF NOT EXISTS Flights (
  Flight_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Aircraft_ID INTEGER, 
  Flight_num INTEGER,
  Depart_city TEXT,
  Destination TEXT,
  Date DATETIME,
  FOREIGN KEY(Aircraft_ID) REFERENCES Aircraft(Aircraft_ID)
)""")

#Many-to-many table 
c.execute("""CREATE TABLE IF NOT EXISTS Pilot_flights (
  PF_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Flights_ID INTEGER,
  Pilot_ID INTEGER,
  FOREIGN KEY(Flights_ID) REFERENCES Flights(Flights_ID),
  FOREIGN KEY(Pilot_ID) REFERENCES Pilots(Pilot_ID)
)""")


################################ Insert data #####################################

######## Pilots ####################
many_pilots = [
  ('Allen Clark', 45, 50000),
  ('Harry Part', 34, 100000),
  ('Mark Smith', 85, 250000),
  ('David Johnson', 23, 19000),
  ('Larry David', 37, 19000),
  ('Selina Kyle', 18, 19000),
  ('Susan Johnson', 34, 19000)
]

c.executemany("INSERT INTO Pilots (Name, Age, Salary) VALUES (?,?,?)", many_pilots)


####### Aircrafts #################

c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('British Airways', '250')")
c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('American Airlines', '250')")
c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('Emirates', '230')")
c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('Qatar Airways','100')")
c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('Japan Airways','400')")
c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('Air France','100')")
c.execute("INSERT INTO Aircrafts (Name, Capacity) VALUES ('Air India','235')")


####### flights ###################

many_flights = [
  #('Aircraft_ID', 'Flight_num', 'Depart_city', 'Destination', 'Date'),
  (1, 23, 'London', 'New York', '2022-07-01 20:30:00'),
  (2, 17, 'Delhi', 'Bangkok', '2022-07-12 11:30:00'),
  (3, 28, 'Cairo', 'Sao Paulo', '2021-01-26 18:45:00'),
  (4, 45, 'Mumbai', 'Goa', '2022-02-14 19:30:00'),
  (7, 67, 'Shanghai', 'Tokyo', '2022-09-18 09:15:00'),
]

c.executemany("INSERT INTO Flights (Aircraft_ID, Flight_num, Depart_city, Destination, Date) VALUES (?,?,?,?,?)", many_flights)

####### Join table for many to many relationship ################

PF_assignment = [
  ('1', '2'),
  ('1', '3'),
  ('2', '1'),
  ('5', '4'),
  ('7', '5'),
  ('2', '4'),
  ('4', '4'),
  ('6', '3')
]

c.executemany("INSERT INTO Pilot_flights (Flights_ID, Pilot_ID) VALUES (?,?)", PF_assignment)


##################################### FUNCTIONS #############################################

#Displays pilot table 
def display_pilots():
  print("Pilots Table")
  df = pd.read_sql_query("select * from Pilots", conn)
  print(df)

#Displays aircrafts table 
def display_aircrafts():
  print("Aircrafts Table")
  df = pd.read_sql_query("select * from Aircrafts", conn)
  print(df)

#Displays flights table 
def display_flights():
  print("Flights Table")
  df = pd.read_sql_query("select * from flights", conn)
  print(df)

#Displays pilot flight assignments table 
def display_PF():
  print("Pilot Assignment Table")
  df = pd.read_sql_query("select * from Pilot_flights", conn)
  print(df)


  
######### Add record ############
#Takes in arguments which will be inputed by the user

#Adds record to pilot table

def add_pilot(name,Age,Salary):
  c.execute("INSERT INTO Pilots VALUES(?,?,?,?)", (None,name,Age,Salary))
  conn.commit()
  display_pilots()


#Adds record to aircrafts table
def add_aircraft(Name, Capacity):
  c.execute("INSERT INTO Aircrafts VALUES(?,?,?)", (None,Name,Capacity))
  conn.commit()
  display_aircrafts()

#Adds record to flight table
def add_flight(Aircraft_ID, Flight_Num, Depart_city, Destination, Date):
  c.execute("INSERT INTO flights VALUES(?,?,?,?,?,?)", (None,Aircraft_ID,Flight_Num,Depart_city,Destination,Date))
  conn.commit()
  display_flights()

#Adds record to pilot flight assignement table
def add_pf(Flights_ID,Pilots_ID):
  c.execute("INSERT INTO Pilot_flights VALUES(?,?,?)", (None,Flights_ID,Pilots_ID))
  conn.commit()
  display_PF()


  
####### Delete Record ########

#Deletes record from Pilot table based on PK
def delete_pilot(Pilot_ID):
  c.execute(f'DELETE FROM Pilots WHERE Pilot_ID= {Pilot_ID}')
  conn.commit()
  display_pilots()

#Deletes record from aircraft table based on PK
def delete_aircraft(Aircraft_ID):
  c.execute(f'DELETE FROM Aircrafts WHERE Aircraft_ID= {Aircraft_ID}')
  conn.commit()
  display_aircrafts()

#Deletes record from flights table based on PK
def delete_flight(Flight_ID):
  c.execute(f'DELETE FROM Flights WHERE Flight_ID= {Flight_ID}')
  conn.commit()
  display_flights() 

#Deletes record from Pilot flight assignement table based on PK
def delete_pf(PF_ID):
  c.execute(f'DELETE FROM Pilot_flights WHERE PF_ID= {PF_ID}')
  conn.commit()
  display_PF() 


######## Modify Record ######### 

#Update pilot record by taking in arguments from user based on 
#which coloumn they want to change 
def update_pilot(coloumn,new,Pilot_ID):
  c.execute(f"UPDATE PILOTS SET {coloumn} = '{new}' WHERE Pilot_ID = {Pilot_ID}")
  conn.commit()
  display_pilots()

#Update aircraft record by taking in arguments from user based on 
#which coloumn they want to change 
def update_aircraft(coloumn,new,Aircraft_ID):
  c.execute(f"UPDATE Aircrafts SET {coloumn} = '{new}' WHERE Aircraft_ID = {Aircraft_ID}")
  conn.commit()
  display_aircrafts()

#Update flight record by taking in arguments from user based on 
#which coloumn they want to change 
def update_flight(coloumn,new,flight_ID):
  c.execute(f"UPDATE Flights SET {coloumn} = '{new}' WHERE Flight_ID = {flight_ID}")
  conn.commit()
  display_flights()

#Update pilot flight assignement record by taking in arguments from user based on 
#which coloumn they want to change 
def update_pf(coloumn,new,pf_ID):
  c.execute(f"UPDATE Pilot_flights SET {coloumn} = '{new}' WHERE PF_ID = {pf_ID}")
  conn.commit()
  display_PF()


############ SELECT coloumn functions ##################

#Select specific coloumns from table based on users request
def search_pilots(coloumns):
  df = pd.read_sql_query(f"SELECT {coloumns} FROM Pilots", conn)
  print(df)

def search_aircrafts(coloumns):
  df = pd.read_sql_query(f"SELECT {coloumns} FROM Aircrafts", conn)
  print(df)

def search_flights(coloumns):
  df = pd.read_sql_query(f"SELECT {coloumns} FROM Flights", conn)
  print(df)

def search_pf(coloumns):
  df = pd.read_sql_query(f"SELECT {coloumns} FROM Pilot_flights", conn)
  print(df)
    

#### Search funtions ########

#Custom function for more specific queries 
def custom_pilots(condition):
  results = c.execute(f"SELECT * FROM Pilots WHERE {condition} FROM PILOTS")
  results = c.fetchall()
  for results in results:
    print(results)

# results = c.execute("SELECT * FROM Pilots WHERE Name = 'john doe'")
# results = c.fetchall()
# for results in results:
#   print(results)

  
  
#Function that lists all the tables in the database 
def table_list():
    print('1 - Pilots')
    print('2 - Aircrafts')
    print('3 - Flights')
    print('4 - Pilot flight assignment')

#Command line interface that will be used to interact with the database 
def main_menu():
  print('\nPlease choose your desired action and then enter the necessary number.')
  print('1 - Select/View Tables')
  print('2 - Insert Data')
  print('3 - Update Data')
  print('4 - Delete Data')
  print('5 - Quit System\n')

  #Reading the users input from the previous options
  cmd = input()

  if (cmd=='1'): 
    print("Enter 1 to Select data from tables: ")
    print("Enter 2 to view tables: ")
    cmd2 = input()
    if (cmd2=='1'): #Select data from tables
      print("From which table do you want to select data")
      table_list()
      cmd=input()
      if(cmd=='1'): #Select data from the pilots table
        display_pilots()
        coloumns = input("Enter the coloumn names you would like to view seperated by commas: ")
        search_pilots(coloumns)
        main_menu()
      elif(cmd=='2'): #Select data from the aircrafts table
        display_aircrafts() 
        coloumns = input("Enter the coloumn names you would like to view seperated by commas: ")
        search_aircrafts(coloumns)
        main_menu()
      elif(cmd=='3'): #Select data from the flights table
        display_flights() 
        coloumns = input("Enter the coloumn names you would like to view seperated by commas: ")
        search_flights(coloumns)
        main_menu()
      elif(cmd=='4'):  #Select data from the pilots flights assignment table
        display_PF()
        coloumns = input("Enter the coloumn names you would like to view seperated by commas: ")
        search_pf(coloumns)
        main_menu()
      else:
        print("Unrecognised input")
        main_menu()
    elif (cmd2=='2'): #View database tables
      print('Which table do you want to view? - Enter the corresponding number')
      table_list()
      cmd=input()
      if(cmd=='1'): #Displays pilot table
        display_pilots()
        main_menu()
      elif(cmd=='2'): #Displays aircrafts table
        display_aircrafts()
        main_menu()
      elif(cmd=='3'): #Displays flights table
        display_flights()
        main_menu()
      elif(cmd=='4'): #Displays pilot flights assignment table
        display_PF()
        main_menu()
      else:
        print("Unrecognised input") #If invalid command then return back to main menu 
        main_menu()
  elif (cmd == '2'): #Add record to database
    print("In which table do you want to add a record? - Enter the corresponding number")
    table_list()
    cmd = input()
    if(cmd=='1'): #Adds record to the pilot table
      name = input('Name: ')
      Age = input('Age: ')
      Salary = input('Enter Salary: ')
      add_pilot(name,Age, Salary)
      main_menu()
    elif(cmd=='2'): #Adds record to the aircraft table
      Name = input("Name of Aircraft: ")
      Capacity = input("Capacity: ")
      add_aircraft(Name, Capacity)
      main_menu()
    elif(cmd=='3'): #Adds record to the flights table
      Aircraft_ID = input("Aircraft ID: ")
      Flight_Num = input("Flight Number: ")
      Depart_city = input("Departure city: ")
      Destination = input("Destination: ")
      Date = input("Date (YYYY-MM-DD HH:MM:SS): ")
      add_flight(Aircraft_ID, Flight_Num, Depart_city, Destination, Date)
      main_menu()
    elif(cmd=='4'): #Adds record to the pilot flights assignement table
      Flights_ID = input("Flight ID: ")
      Pilots_ID = input("Pilot ID: ")
      add_pf(Flights_ID,Pilots_ID)
      main_menu()
  elif (cmd == '3'): #Modify data
    print("In which table do you want to modify a record? - Enter the corresponding number")
    table_list()
    cmd = input()
    if(cmd=='1'): #Modifies pilot data based on the coloumn the users wants to change 
      display_pilots()
      Pilot_ID = input('Enter the Pilot_ID of the pilot you want to update: ')
      coloumn = input('Enter the name of the coloumn you would like to update: ')
      new = input('Enter the new value: ')
      update_pilot(coloumn,new,Pilot_ID)
      main_menu()
    elif(cmd=='2'): #Modifies aircraft data based on the coloumn the users wants to change 
      display_aircrafts()
      Aircraft_ID = input('Enter the Aircraft_ID of the aircraft you want to update: ')
      coloumn = input('Enter the name of the coloumn you would like to update: ')
      new = input('Enter the new value: ')
      update_aircraft(coloumn,new,Aircraft_ID)
      main_menu()
    elif(cmd=='3'): #Modifies flights data based on the coloumn the users wants to change 
      display_flights()
      flight_ID = input('Enter the Flight_ID of the flight you want to update: ')
      coloumn = input('Enter the name of the coloumn you would like to update: ')
      new = input('Enter the new value: ')
      update_flight(coloumn,new,flight_ID)
      main_menu()
    elif(cmd=='4'): #Modifies pilot flight assignment data based on the coloumn the users wants to change 
      display_PF()
      pf_ID = input('Enter the PF_ID of the Pilot-flight you want to update: ')
      coloumn = input('Enter the name of the coloumn you would like to update: ')
      new = input('Enter the new value: ')
      update_pf(coloumn,new,pf_ID)
      main_menu()
  elif (cmd == '4'): #Delete Data  
    print("In which table do you want to delete a record? - Enter the corresponding number")
    table_list()
    cmd = input()
    if(cmd=='1'): 
      display_pilots() #Deletes record from pilot table based on the PK chosen 
      Pilot_ID = input("Enter the Pilot_ID you would like to delete: ")
      delete_pilot(Pilot_ID)
      main_menu()
    elif(cmd=='2'): #Deletes record from aircrafts table based on the PK chosen 
      display_aircrafts()
      Aircraft_ID = input("Enter the Aircraft_ID you would like to delete: ")
      delete_aircraft(Aircraft_ID)
      main_menu()
    elif(cmd=='3'): #Deletes record from flights table based on the PK chosen 
      display_flights()
      Flight_ID = input("Enter the Flight_ID you would like to delete: ")
      delete_flight(Flight_ID)
      main_menu()
    elif(cmd=='4'): #Deletes record from pilot flight assignment table based on the PK chosen 
      display_PF()
      PF_ID = input("Enter the PF_ID you would like to delete: ")
      delete_pf(PF_ID)
      main_menu()
  elif (cmd == '5'): #Quit system
    cmd = input("Do you want to save changes? - (y/n) ")
    quit_system(cmd)
  else:
    print('Input unrecognised') #If unrecognised operator then return to main menu
    main_menu()

#function saves the database and closes it, or return back to the main menu 
def quit_system(cmd):
  if (cmd=='y'):
    print("Changes saved")
    print("Database closed")
    conn.commit()
    conn.close()
  elif (cmd=='n'):
    main_menu()
  else:
    None
  



main_menu()

conn.close()
#Closing the database