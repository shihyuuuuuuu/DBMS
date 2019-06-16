#!/usr/bin/env python3
import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,\
        QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QTableWidget, QTableWidgetItem


class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.first = True
        
        # SQL commands for the buttons
        self.selectsql = """SELECT * FROM Player"""
        self.inssql = """INSERT INTO Player (
         Age,
         Birth_date,
         Num,
         PName,
         TName)
         VALUES (21, '19970723', 22, 'TengShihYu', 'Yulon');"""
        self.delsql = """DELETE FROM Player WHERE PName='TengShihYu'"""
        self.updsql = """UPDATE Player SET TName='TWBeer' WHERE PName='ChiangYuAn'"""
        self.insql = """SELECT Age, Birth_date, PName, Team.TName, Coach
FROM Player, Team
WHERE PName IN
        (SELECT PName
        From Player
        WHERE Age > 26) AND Player.TName=Team.TName;"""
        self.notinsql = """SELECT Age, Birth_date, PName, Team.TName, Coach
FROM Player, Team
WHERE PName NOT IN
        (SELECT PName
        From Player
        WHERE Age > 26) AND Player.TName=Team.TName;"""
        self.existsql = """SELECT Team.Tname, Coach, CName
        FROM Team, Company
        WHERE EXISTS(SELECT * 
            FROM Company
            WHERE Location=CName) AND Team.TName=Company.tName"""
        self.notexistsql = """SELECT  Num_of_seats, SName
FROM Stadium
WHERE NOT EXISTS(SELECT *
	FROM Game
	WHERE Stadium.SName=Game.SName)"""
        self.aggrsql = """SELECT Max(Age), Sum(Age), Min(Age), Avg(Age), Count(*)
FROM Player"""
        self.havingsql = """SELECT Player.TName
FROM Player, Team
WHERE Player.TName=Team.TName
GROUP BY Player.TName
HAVING COUNT(*) > 1"""
        
        self.h2 = QVBoxLayout()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.resize(600, 600)
        self.setWindowTitle("Database Project")

        self.sql_label = QLabel()
        self.sql_label.setText("請輸入SQL指令")

        # Create input text box and the 'run' button and output label
        self.text_sql = QTextEdit()
        self.btn_runsql = QPushButton()
        self.btn_runsql.setText("執行SQL!")
        self.btn_runsql.setStyleSheet("background-color: green")
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.out_label = QLabel()
        self.layout = QVBoxLayout()
        h1 = QVBoxLayout()
        h1.addWidget(self.sql_label)
        h1.addWidget(self.text_sql)
        h1.addWidget(self.btn_runsql)
        h1.addWidget(self.out_label)
        #h1.addWidget(self.text_output)


        # Create basic queries buttons
        self.select_btn = QPushButton()
        self.insert_btn = QPushButton()
        self.update_btn = QPushButton()
        self.delete_btn = QPushButton()
        self.select_btn.setText("Select")
        self.insert_btn.setText("Insert")
        self.update_btn.setText("Update")
        self.delete_btn.setText("Delete")
        basic_queries = QHBoxLayout()
        basic_queries.addWidget(self.select_btn)
        basic_queries.addWidget(self.insert_btn)
        basic_queries.addWidget(self.update_btn)
        basic_queries.addWidget(self.delete_btn)

        # Create complex queries buttons
        self.in_btn = QPushButton()
        self.notin_btn = QPushButton()
        self.exist_btn = QPushButton()
        self.notexist_btn = QPushButton()
        self.aggr_btn = QPushButton()
        self.having_btn = QPushButton()
        self.in_btn.setText("In")
        self.notin_btn.setText("Not In")
        self.exist_btn.setText("Exist")
        self.notexist_btn.setText("Not Exist")
        self.aggr_btn.setText("Aggregate")
        self.having_btn.setText("Having")
        h3 = QHBoxLayout()
        h3.addWidget(self.in_btn)
        h3.addWidget(self.notin_btn)
        h3.addWidget(self.exist_btn)
        h3.addWidget(self.notexist_btn)
        h3.addWidget(self.aggr_btn)
        h3.addWidget(self.having_btn)
        
        # Connect the buttons to their functions
        self.select_btn.clicked.connect(lambda: self.complex(self.selectsql))
        self.insert_btn.clicked.connect(lambda: self.complex(self.inssql))
        self.delete_btn.clicked.connect(lambda: self.complex(self.delsql))
        self.update_btn.clicked.connect(lambda: self.complex(self.updsql))
        self.in_btn.clicked.connect(lambda: self.complex(self.insql))
        self.notin_btn.clicked.connect(lambda: self.complex(self.notinsql))
        self.exist_btn.clicked.connect(lambda: self.complex(self.existsql))
        self.notexist_btn.clicked.connect(lambda: self.complex(self.notexistsql))
        self.aggr_btn.clicked.connect(lambda: self.complex(self.aggrsql))
        self.having_btn.clicked.connect(lambda: self.complex(self.havingsql))

        
        self.layout.addLayout(h1)
        self.layout.addLayout(basic_queries)
        self.layout.addLayout(h3)
        self.setLayout(self.layout)
        self.btn_runsql.clicked.connect(lambda: self.run(0))
    
    def complex(self, signal):
        self.text_sql.setText(signal)
        self.run(signal)


    def run(self, sql):
        if sql == 0:
            input_sql = self.text_sql.toPlainText()
        else:
            input_sql = sql
        try:
            cursor.execute(input_sql)
            result = cursor.fetchall()
            db.commit()
            if input_sql.split()[0] != 'SELECT':
                self.out_label.setText(input_sql.split()[0] + ' Success!')
            else:
                self.out_label.setText("")
                text=""
                for r in result:
                    text = text + str(r) + "\n"
                self.text_output.setText(text)
                row = len(result)
                col = len(result[0])
                if self.first  == False:
                    self.layout.removeItem(self.h2)
                else:
                    self.first = False

                self.myTable = QTableWidget(row,col)
                for i in range(row):
                    for j in range(col):
                        newItem = QTableWidgetItem(str(result[i][j]))
                        self.myTable.setItem(i, j, newItem)
                self.h2 = QVBoxLayout()
                self.h2.addWidget(self.myTable)
                self.layout.addLayout(self.h2)
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            self.text_output.setText(str(e))
            db.rollback()


if __name__ == "__main__":
    db = pymysql.connect("localhost", "root", "password", "Basketball")
    cursor = db.cursor()
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())
    db.close()
