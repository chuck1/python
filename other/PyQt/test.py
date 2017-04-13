#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

class DragLabel(QLabel):
    def __init__(self, text, w):
        super().__init__(text, w)

        self.setAutoFillBackground(True)    
        p = self.palette()
        p.setColor(self.backgroundRole(), PyQt5.QtCore.Qt.blue)
        self.setPalette(p)
        

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == PyQt5.QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            
            print('press pos',self.__mousePressPos)

        super(DragLabel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragLabel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        print('mouse release')

        if self.__mousePressPos is not None:

            print('self.__mousePressPos is not None')

            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                print('moved.manhattanLength() > 3')
                event.ignore()

                # undo move
                print('undo move')
                self.move(self.mapFromGlobal(self.__mousePressPos))

                return
            
        
        super(DragLabel, self).mouseReleaseEvent(event)

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')

        label1 = DragLabel('label1', self)

        label2 = DragLabel('label2', self)

        hbox = QHBoxLayout()

        hbox.addWidget(label1)
        hbox.addWidget(label2)

        self.setLayout(hbox)

        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    w = Example()

    sys.exit(app.exec_())

