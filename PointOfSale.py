# Dikatso Moshweunyane
# 12 March 2020
# Tutorial 4(Databse Programming)

import sys # imports standard Python sys module
from datetime import*
from PyQt5.QtWidgets import* # imports PyQt5 modules
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3


class POS_GUI(QWidget):
    def __init__(self,parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(250,250,600,300)
        self.setWindowTitle("Point Of Sale") 
        
        # Create Labels 
        self.stock_code = QLabel("Stock Code:")
        self.item = QLabel("Item:")
        self.quantity = QLabel("Quantity:")
        self.brief_description = QLabel("Brief Description:")
        self.sales_price = QLabel("Sales Price:")
        self.error =QLabel("")
        self.stock_codeDisplay = QLabel("")
        self.brief_descriptionDisplay = QLabel("")
        self.sales_priceDisplay = QLabel("")
        
        #Create QLine Edit Boxes
        self.quantityEdit = QLineEdit()
        
        # Create Pushbuttons
        self.quit = QPushButton("Close")
        self.sales = QPushButton("Sales")
        self.ok = QPushButton("OK")
        
        # Create ComboBox
        self.combo = QComboBox()
        self.combo.addItem("")
        self.combo.addItem("Pencil Case")
        self.combo.addItem("Study Lamp")
        self.combo.addItem("Casio Calculator")
        self.combo.addItem("Bic Ballpen") 
        self.combo.addItem("Desk Calender")
        self.combo.addItem("Ruler")
        self.combo.addItem("Board Marker")
        self.combo.addItem("Water Bottle")
        self.combo.addItem("Stapler")
        self.combo.addItem("Prestik")
        
        # Inserting Labels  & QLineEdits
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(self.stock_code)
        upper_layout.addWidget(self.stock_codeDisplay)
        upper_layout.addWidget(self.item)
        upper_layout.addWidget(self.combo)
        upper_layout.addWidget(self.quantity)
        upper_layout.addWidget(self.quantityEdit)
        upper_layout.addWidget(self.error)
        upper_layout.addWidget(self.brief_description)
        upper_layout.addWidget(self.brief_descriptionDisplay)
        upper_layout.addWidget(self.sales_price)
        upper_layout.addWidget(self.sales_priceDisplay)
        upper_widget = QWidget()
        upper_widget.setLayout(upper_layout)
        
        # Inserting Push Buttons
        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.quit)
        lower_layout.addWidget(self.sales)
        lower_layout.addWidget(self.ok)
        lower_widget = QWidget()
        lower_widget.setLayout(lower_layout)
        
        # Merging Layouts
        main_layout = QVBoxLayout()
        main_layout.addWidget(upper_widget)
        main_layout.addWidget(lower_widget)
        self.setLayout(main_layout)
        
        # Connecting slots to signals
        self.quit.clicked.connect(self.clicked_close)
        self.combo.currentTextChanged.connect(self.combo_box)
        self.ok.clicked.connect(self.ok_clicked)
        self.sales.clicked.connect(self.sales_dialog)
       
        # Connecting GUI to database
        self.database = sqlite3.connect("Database.db")
        
        #Set colour 
        self.setPalette(QPalette(QColor("dark red")))
        
        # Creating Cursors
        stock_cursor = self.database.execute('select * from Stock')
        sales_cursor = self.database.execute('select * from Sales')
        self.stock_results = stock_cursor.fetchall()
        self.sales_results = sales_cursor.fetchall()
        database = self.database.cursor()

    def combo_box(self):
        ProductLocation = (self.combo.currentIndex()) - 1              # Gets Index Of Selected ComboBox Item
        self.stock_codeDisplay.setText(str(self.stock_results[ProductLocation][0]))         #Displays the stock code
        self.brief_descriptionDisplay.setText(str(self.stock_results[ProductLocation][2]))  # Displays the Brief Description
        self.sales_priceDisplay.setText("R"+str(self.stock_results[ProductLocation][4]))    # Displays the price display
    
    def ok_clicked(self):
        try:
            ProductLocation = (self.combo.currentIndex()) - 1       # Gets Index Of Selected ComboBox Item
            stock_quantity = self.stock_results[ProductLocation][5] # Gets the product's stock quantity
            input_quantity = int(self.quantityEdit.displayText())
            if input_quantity <= stock_quantity and input_quantity > 0:
                new_quantity = int(stock_quantity - input_quantity)
                self.database.execute('update Stock set Quantity_Stock = (?) where Item_Name = (?)',(new_quantity,self.combo.currentText()))  # Updates database with new quantity
                self.database.commit()
                time_ = str(datetime.now())
                time_ = time_[:time_.find(".")]
                self.database.execute('insert into Sales values(?,?,?)',(str(self.stock_results[ProductLocation][0]),input_quantity,time_))  #  Inserts data into the Sales table
                self.error.clear()
                self.database.commit()
                
            elif input_quantity < 0 :
                self.error.setText("!!!!!!PLEASE ENTER A VALID NUMBER!!!!!!")
                self.database.commit()
            
            elif input_quantity > stock_quantity:
                self.error.setText("WE ONLY HAVE " + str(stock_quantity) +" AVAILABLE")
                self.database.commit()
                    
        except ValueError or NameError:
            self.error.setText("!!!!!!PLEASE ENTER AN INTEGER!!!!!!")
            self.database.commit()
        
        finally:
            self.quantityEdit.clear()
            
    def sales_dialog(self):
        try:
            self.dialog = QDialog()
            self.dialog.setGeometry(250,250,350,300)
            self.dialog.setWindowTitle("Sales Report")
            
            # Sets colour
            self.dialog.setPalette(QPalette(QColor("dark red")))
            
            # Connects to database
            database = sqlite3.connect("Database.db")
            
            # Create Labels
            self.num_sold = QLabel("Total Number of Items Sold:")
            self.num_SoldDisplay = QLabel("")
            self.cost_price = QLabel("Total Cost Price:")
            self.cost_priceDisplay = QLabel("")
            self.sales_price = QLabel("Total Sales Price:")
            self.sales_priceDisplay = QLabel("")
            self.profit = QLabel("Total Profit:")
            self.profitDisplay = QLabel("")
            
            # Creates VBox
            vbox = QVBoxLayout()
            vbox.addWidget(self.num_sold)
            vbox.addWidget(self.num_SoldDisplay)
            vbox.addWidget(self.cost_price)
            vbox.addWidget(self.cost_priceDisplay)
            vbox.addWidget(self.sales_price)
            vbox.addWidget(self.sales_priceDisplay)
            vbox.addWidget(self.profit)
            vbox.addWidget(self.profitDisplay)
            vbox_widget = QWidget()
            self.dialog.setLayout(vbox)
            
            # Creates cursors
            stock_cursor = database.execute('select * from Stock')
            sales_cursor = database.execute('select * from Sales')
            self.stock_results = stock_cursor.fetchall()
            self.sales_results = sales_cursor.fetchall()
            database_cursor = database.cursor()
            

            
            def saleprice(stock_code):  # Gets salesprice from database
                database_cursor.execute("SELECT Sales_Price FROM Stock WHERE Stock_Code = :Stock_Code", {"Stock_Code":stock_code})
                return database_cursor.fetchone()[0]
            
            def costprice(stock_code):  # Gets costprice from database
                database_cursor.execute("SELECT Cost_Prices FROM Stock WHERE Stock_Code = :Stock_Code", {"Stock_Code":stock_code})
                return database_cursor.fetchone()[0]
            
            # Creating Total Variables
            self.numSold = 0
            self.costPrice = 0
            self.salesPrice = 0
            self.total_profit = 0
            self.counter = 0
            
            # Calculates the length of database list
            list_len = len(self.sales_results)             
            while True:
                self.stock_code = self.sales_results[self.counter][0]  # Gets the stock code
                self.quantity = self.sales_results[self.counter][1]  # Gets the number of stock sold
                self.quantity = int(self.quantity)
                self.costPrice += costprice(self.stock_code)*self.quantity
                self.salesPrice += saleprice(self.stock_code)*self.quantity
                self.counter += 1
                self.numSold += self.quantity

                if self.counter == list_len:
                    self.total_profit = self.salesPrice - self.costPrice   # Calculates profit
                    self.num_SoldDisplay.setText(str(self.numSold)+ " Items")
                    self.cost_priceDisplay.setText("R" + str(self.costPrice))
                    self.sales_priceDisplay.setText("R" + str(self.salesPrice))  
                    self.profitDisplay.setText("R" + str(self.total_profit))
                    break
            self.error.clear()
            self.dialog.show()
            
        except:
            self.error.setText("!!!!!!SALES REPORT IS EMPTY!!!!!!")
            
    def clicked_close(self):
        self.close()    # Closes the window
    

def main():
    app = QApplication(sys.argv)
    abs_widget = POS_GUI()
    abs_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()