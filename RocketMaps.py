from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import (QWidget, QApplication, QGridLayout)
import os
import sys

class RocketMap(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.map_view = Map({'pointRadius':'100'})
        self.grid.addWidget(self.map_view, 1, 1)


class Map(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, params):
        super().__init__()
        self.params={}
        try:
            self.params.update(params)
        except Exception as e:
            print('[MapParamsError]', e)
        url_params = QtCore.QUrlQuery();
        for k,v in self.params.items():
            url_params.addQueryItem(str(k),str(v))
        dir = os.getcwd()+"/maps/main.html"
        url = QtCore.QUrl(dir)
        url.setQuery(url_params)
        self.setUrl(url)

    def addPointToPath(self, x, y, color):
        comand = 'addPointToPath("{}", "{}", "{}");'.format(x, y, color)
        print(comand)
        self.page().runJavaScript(comand)


app=QApplication(sys.argv)
win=RocketMap()
win.show()
app.exec_()
