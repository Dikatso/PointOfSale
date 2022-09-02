# Dikatso Moshweunyane
# 12 March 2020
# Tutorial 4(Databse Programming)

import sqlite3

database = sqlite3.connect("Database.db")   # Connects to the database

# Creating tables in database
database.execute("""CREATE TABLE Stock(
Stock_Code TEXT,
Item_Name TEXT,
Brief_Description TEXT,
Cost_Prices INT,
Sales_Price INT,
Quantity_Stock INT
)""")

database.execute("""CREATE TABLE Sales(
Stock_Code TEXT,
Quantity TEXT,
Date_Time TEXT
)""")

# Adding stock into the database
database.execute('insert into Stock values("P1","Pencil Case","A case for carrying pencils , pens , rubbers , etc ",10,20,50)')
database.execute('insert into Stock values("P2","Study Lamp","A small lamp that you keep on a desk or table.",80,100,50)')
database.execute('insert into Stock values("P3","Casio Calculator","An electronic calculator that can handle trigonometric, exponential and often other advanced functions.",450,500,50)')
database.execute('insert into Stock values("P4","Bic Ballpen","A pen that has a small metal ball as the point of transfer of ink to paper.",7,12,50)')
database.execute('insert into Stock values("P5","Desk Calender","A loose-leaf calendar containing one or two pages for each day, with spaces for notes.",35,40,50)')
database.execute('insert into Stock values("P6","Ruler","A material having a straight edge marked off in inches or centimeters",1,2,50)')
database.execute('insert into Stock values("P7","Whiteboard","A panel covered with white, glossy plastic for writing on with erasable markers.",25,32,50)')
database.execute('insert into Stock values("P8","Water Bottle","A small bottle containing water for drinking.",92,134,50)')
database.execute('insert into Stock values("P9","Stapler","A small device that you can hold in your hand or use on a table to push staples through pieces.",120,150,50)')
database.execute('insert into Stock values("P10","Prestik","A rubber-like temporary adhesive used to join paper.",14,25,50)')



database.commit()
database.close()