import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, 
                             QHBoxLayout, QVBoxLayout, QWidget, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd

#Creating table view
class DataFrameModel(QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self._data = df

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            if orientation == Qt.Vertical:
                return self._data.index[section]
        return None


#Creating App
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FM Transfer Helper')
        self.central_wideget = QWidget()
        self.setCentralWidget(self.central_wideget)
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        #Create output field
        self.output_field = QTableView()

        #Create buttons
        buttons = ['Winger', 'Advanced Forward', 'Box to box Midfielder', 'Roaming Playmaker', 'Attacking fullback', 
                   'Inverted Wingback', 'Ball-Playing Defender']
        
        self.stat_widget = QWidget()
        self.winger_button = QPushButton('Winger',self)
        self.fullback_button =QPushButton('Fullback',self)
        self.dm_button = QPushButton('Defensive Midfielder', self)
        self.pm_button = QPushButton('Playmaker', self)
        self.def_button = QPushButton('Defender', self)
        self.striker_button = QPushButton('Striker', self)
        self.gk_button = QPushButton('Goalkeeper', self)

        #load functions
        self.load_data()
        self.winger_scoring()
        self.fullback_scoring()
        self.dm_scoring()
        self.pm_scoring()
        self.def_scoring()
        self.striker_scoring()
        self.gk_scoring()
        self.initUI()


    #UI function
    def initUI(self):
        self.hbox.addWidget(self.output_field)
        self.vbox.addWidget(self.winger_button)
        self.winger_button.clicked.connect(lambda: self.output_field.setModel(self.winger_score))
        self.vbox.addWidget(self.fullback_button)
        self.fullback_button.clicked.connect(lambda: self.output_field.setModel(self.fullback_score))
        self.vbox.addWidget(self.dm_button)
        self.dm_button.clicked.connect(lambda: self.output_field.setModel(self.dm_score))
        self.vbox.addWidget(self.pm_button)
        self.pm_button.clicked.connect(lambda: self.output_field.setModel(self.pm_score))
        self.vbox.addWidget(self.striker_button)
        self.striker_button.clicked.connect( lambda: self.output_field.setModel(self.striker_score))
        self.vbox.addWidget(self.def_button)
        self.def_button.clicked.connect(lambda: self.output_field.setModel(self.def_score))
        self.vbox.addWidget(self.gk_button)
        self.gk_button.clicked.connect(lambda: self.output_field.setModel(self.gk_score))
        self.stat_widget.setLayout(self.vbox)
        self.hbox.addWidget(self.stat_widget)
        self.central_wideget.setLayout(self.hbox)
    
    #role scoring functions
    def winger_scoring(self):
        self.df["Score"] = self.df["Drb/90"] + self.df['Ch C/90'] + self.df['Cr C/90'] + self.df['xG-OP'] + self.df['NP0xG/90'] + self.df['xA/90'] + self.df['Cr C/A']
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.winger_score = DataFrameModel(self.sorted_ranking.head(20))

    def fullback_scoring(self):
        self.df["Score"] = self.df["Drb/90"] + self.df['Ch C/90'] + self.df['Pr passes/90'] + self.df['Tck R'] + self.df['Blk/90'] + self.df['xA/90'] + self.df['Int/90']
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.fullback_score = DataFrameModel(self.sorted_ranking.head(20))

    def dm_scoring(self):
        self.df["Score"] = self.df["Tck R"] + self.df['K Tck/90'] + self.df['Pres A/90'] + self.df['Pr passes/90'] + self.df['Int/90'] - self.df['Poss Lost/90'] + self.df['Poss Won/90'] + self.df['Pas %'] + self.df['Tck/90']
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.dm_score = DataFrameModel(self.sorted_ranking.head(20))

    def pm_scoring(self):
        self.df["Score"] = self.df["K Ps/90"] + self.df['Pas %'] + self.df['Pr passes/90'] + self.df['Drb/90'] + self.df['Dist/90'] + self.df['xA/90'] + self.df['Ch C/90']
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.pm_score = DataFrameModel(self.sorted_ranking.head(20))

    def def_scoring(self):
        self.df["Score"] = self.df["Tck R"] + self.df['K Tck/90'] + self.df['Hdr %'] + self.df['K Hdrs/90'] + self.df['Pr passes/90'] + self.df['Poss Won/90'] + self.df['Pas %']
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.def_score = DataFrameModel(self.sorted_ranking.head(20))

    def striker_scoring(self):
        self.df["Score"] = self.df["xG/90"] + self.df['xG-OP'] + self.df['Drb/90'] + self.df['xG/shot'] + self.df['Conv %'] + self.df['Gls/90'] + self.df['NP0xG/90'] + self.df['Hdr %'] 
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.striker_score = DataFrameModel(self.sorted_ranking.head(20))

    def gk_scoring(self):
        self.df["Score"] = self.df["Sv %"] + self.df['xGP/90'] + self.df['xSv %'] + self.df['Pas %'] + self.df['Pens Saved Ratio'] -self.df['Gl Mst']
        self.ranking = self.df[["Name", 'Transfer Value', 'Score']].copy()
        self.sorted_ranking = self.ranking.sort_values(by="Score", ascending=False)
        self.gk_score = DataFrameModel(self.sorted_ranking.head(20))


    #setting up the datafeme
    def load_data(self):
        self.df = pd.read_csv("qwe.csv", encoding = "ANSI")
       

        #Editing data
        def max_value(value):
            if isinstance(value, float):
                return value
            else:
                if value == "Not for Sale":
                    return 'N/A'
                if "-" in value and "K" not in value:
                    first = value.split("-")
                    second = first[1].replace("$","")
                    third = second.replace("M","")
                    return float(third)
                if "K" in value:
                    return 0
                else:
                    first = value.replace("$","")
                    second = first.replace("M","")
                    return float(second)

        def nomi(value):
            if isinstance(value, float):
                return value
            else:
                new = value.replace('mi','')
                return float(new)
    

        new_value = []
        for i in self.df[ 'Transfer Value']:
            new_value.append(max_value(i))
        self.df[ 'Transfer Value'] = new_value 

        new_dist = []
        for i in self.df['Dist/90']:
            new_dist.append(nomi(i))
        self.df["Dist/90"] = new_dist
        self.df["Score"] = 0

        self.df = self.df.fillna(0)
    
    
    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

main()