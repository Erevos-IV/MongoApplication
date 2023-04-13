import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QTextOption
from PyQt5.QtCore import Qt
from pymongo import MongoClient
import pandas as pd
import time

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://bill:bill@clusterreviews.eb583st.mongodb.net/?retryWrites=true&w=majority")
db = client['Review']
collection = db['reviews']

class ReviewQueryApp(QWidget):

    def __init__(self):
        super().__init__()

        # Create UI elements
        self.county_label = QLabel('County Name:')
        self.county_edit = QLineEdit()
        self.county_button = QPushButton('Find Shops Per County')
        self.county_button.setStyleSheet("background-color: #4CAF50; color: white")

        self.shop_label = QLabel('Shop Name:')
        self.shop_edit = QLineEdit()
        self.shop_button = QPushButton('Find Reviews Per Shop')
        self.shop_button.setStyleSheet("background-color: #4CAF50; color: white")

        self.output_label = QLabel('Output:')
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #f2f2f2")
        self.output_text.setTextInteractionFlags(self.output_text.textInteractionFlags() | Qt.TextSelectableByMouse)
        self.output_text.setTextInteractionFlags(self.output_text.textInteractionFlags() | Qt.TextSelectableByKeyboard)
        self.output_text.setWordWrapMode(QTextOption.WrapAnywhere)

        self.exit_button = QPushButton('Exit')
        self.exit_button.setStyleSheet("background-color: #f44336; color: white")

        self.time_label = QLabel('Elapsed Time:')
        self.time_value = QLabel()

        # Add UI elements to layout
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.county_label)
        vbox1.addWidget(self.county_edit)
        vbox1.addWidget(self.county_button)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.shop_label)
        vbox2.addWidget(self.shop_edit)
        vbox2.addWidget(self.shop_button)

        hbox1 = QHBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.output_label)
        vbox3.addWidget(self.output_text)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.time_label)
        hbox2.addWidget(self.time_value)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.exit_button)

        vbox_main = QVBoxLayout()
        vbox_main.addLayout(hbox1)
        vbox_main.addLayout(vbox3)
        vbox_main.addLayout(hbox2)
        vbox_main.addLayout(hbox3)

        self.setLayout(vbox_main)

        # Connect signals to slots
        self.county_button.clicked.connect(self.find_shops)
        self.shop_button.clicked.connect(self.find_reviews)
        self.exit_button.clicked.connect(self.close)

    def find_shops(self):
        start_time = time.time()
        county = self.county_edit.text()
        shops = collection.find({'County': county}).distinct('Shop')
        df = pd.DataFrame({'Shops': shops})
        self.output_text.setPlainText(df.to_string(index=False).ljust(250))
        elapsed_time = time.time() - start_time
        self.time_value.setText(f"{int(elapsed_time*1000)} ms")
    
    def find_reviews(self):
        shop = self.shop_edit.text().strip()
    
        start_time = time.time()  
    
        reviews = collection.find({'Shop': {'$regex': shop.strip(), '$options': 'i'}}, {'Review': 1})

        

        df = pd.DataFrame(list(reviews))
        if not df.empty:
            df = df[['Review']]
            self.output_text.setPlainText(df.to_string(index=False).ljust(250))
        else:
            self.output_text.setPlainText(f"No reviews found for {shop}.")
        elapsed_time = time.time() - start_time  
        self.time_value.setText(f"{int(elapsed_time*1000)} ms") 



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReviewQueryApp()
    window.setWindowTitle('Review Query App')
    window.show()
    sys.exit(app.exec_())

