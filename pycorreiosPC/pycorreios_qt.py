#!/usr/bin/env python
__title__ = "pycorreios_qt.py"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "12/04/2013"
__versio__ = "0.1"
"""


This file is part of pycorreios.
    copyright : Eduardo dos Santos Pereira
    14 october 2013

    pycorreios is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    pycorreios is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import *
from PyQt4.QtGui import QSound

from pycorreiosUI import Ui_MainWindow, _fromUtf8
from pycorreios import adentregas
import multiprocessing as mpg

#from pyglet.resource import media
#import pygame

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


class DesignerMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)

        QtCore.QObject.connect(self.pushButton,
                               QtCore.SIGNAL("clicked()"),
                               self.starting)
        QtCore.QObject.connect(self.pushButton_2,
                               QtCore.SIGNAL("clicked()"),
                               self.pararMonitoramento)
        QtCore.QObject.connect(self.pushButton_3,
                               QtCore.SIGNAL("clicked()"),
                               self.clearList)

        self.monitorEstatos = None
        self.statusBar().showMessage(
            'Bem vindo ao Sis. de Mon.de Saida Enc. dos Correios')
        self.countEventos = None
        self.TotEventos = None
        self.estatosDoProduto = None
        self.codigos = None
        self.localSom = None
        self.timer = QtCore.QTimer()
        self.playAlarm = None
        self.subprocess = []
        QtCore.QObject.connect(self.timer,
                                QtCore.SIGNAL("timeout()"),
                                self.__verificaFim)
        QtCore.QObject.connect(self, QtCore.SIGNAL('triggered()'),
                                     self.closeEvent)

        #self.webview = QWebView(self.frame)
        #self.webview.setObjectName(_fromUtf8('webview'))
        #self.textBrowser = QtGui.QTextBrowser(self.frame)
        #self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        #self.verticalLayout_2.addWidget(self.webview)

        #self.paginaAguarde = """<HTML>
#<HEAD>
#<TITLE>Bem vindo ao Sistema de Monitoramento</TITLE>
#</HEAD>
#<H1> </H1>
#<FONT face=Arial size=3 color="#000000">
#<b>
#Bem vindo ao Sistema de Monitoramento de saida de encomendas dos correios.
#</b></font>
#<br><br>
#</BODY>
#</HTML>

#"""
        #self.webview.setHtml(self.paginaAguarde)

    def __startingMonitor(self, q, deltaT, rCode):

        monitor = adentregas(rCode, float(deltaT), alarmeLD=False)
        monitor.monitorEntregas()
        self.localSom.value = monitor.mysound

        if(self.estatosDoProduto.value == 'Iniciando Array Est.'):
            self.estatosDoProduto.value = monitor.objetoEstatus +\
                                         ':Codigo:' + monitor.rcode
        else:
            self.estatosDoProduto.value += ';' + monitor.objetoEstatus +\
                                         ':Codigo:' + monitor.rcode

        self.countEventos.value += 1
        self.playAlarm.value = 0

    def __verificaFim(self):
        if(self.TotEventos.value == self.countEventos.value):
            self.statusBar().showMessage('Monitoramentos Finalizados')

            if(self.playAlarm.value < 1):
                self.listWidget.addItems(
                                    self.estatosDoProduto.value.split(';'))
                mixer.init()
                sound = mixer.Sound(r'' + self.localSom.value)
                sound.play()
                #QSound(r'' + self.localSom.value).play()
                self.playAlarm.value += 1

        elif(self.countEventos.value < self.TotEventos.value):

            if(self.estatosDoProduto.value is None):
                pass
            elif(self.estatosDoProduto.value != 'Iniciando Array Est.'):

                estados = self.estatosDoProduto.value.split(';')

                codigos = [estado.split(':')[-1] for estado in estados]

                for i in range(len(codigos)):

                    if(self.codigos is not None and
                        codigos[i] in self.codigos):
                        self.codigos = [cd for cd in self.codigos
                                     if cd != codigos[i]]

                        #self.statusBar().showMessage('Objeto ' +
                                                #str(self.countEventos.value) +
                                                #'. Estatos: ' +
                                                #estados[i])
                        self.listWidget.addItems([estados[i]])
                        #'Saiu para entrega'
                        print estados[i].split(':')[0]

                        if(estados[i].split(':')[0] == 'Saiu para entrega'
                            or estados[i].split(':')[0] == 'Entrega Efetuada'):
                            #mixer.init()
                            #sound = mixer.Sound(r'' + self.localSom.value)
                            #sound.play()
                            QSound(r'' + self.localSom.value).play()
        else:
            self.statusBar().showMessage('Processando, aguarde...')

    def closeEvent(self, event):
        [p.terminate() for p in self.subprocess]
        self.deleteLater()

    def pararMonitoramento(self):
        [p.terminate() for p in self.subprocess]
        self.countEventos.value = 0
        self.playAlarm.value = 0
        self.codigos = None
        print 'Terminar'

    def clearList(self):
        self.listWidget.clear()

    def starting(self):

        #paginaAguarde = """<HTML>
#<HEAD>
#<TITLE>Iniciando o Sistema de Monitoramento</TITLE>
#</HEAD>
#<H1> </H1>
#<FONT face=Arial size=3 color="#000000"><b>
#Sistema de Monitoramento Finalizado</b></font>
#<br><br>
#</BODY>
#</HTML>

#"""
        #self.webview.setHtml(paginaAguarde)

        deltaT = self.spinBox.value()
        codigos = unicode(self.lineEdit.text())
        codigos = codigos.split(',')
        codigos = [codigo for codigo in codigos if codigo != '']
        if(self.codigos is not None):
            codigos = [codigo for codigo in codigos
                                     if not codigo in self.codigos]
        self.codigos = codigos
        self.statusBar().showMessage('Iniciando')
        self.playAlarm = mpg.Value('i', 0)

        self.TotEventos = mpg.Value('i', len(codigos))
        self.countEventos = mpg.Value('i', 0)
        self.estatosDoProduto = mpg.Array('c', 1200)
        self.estatosDoProduto.value = 'Iniciando Array Est.'
        self.localSom = mpg.Array('c', 1200)
        self.timer.start(1000)

        n_process = mpg.cpu_count()

        for codigo in codigos:
            q = mpg.Queue()
            p = mpg.Process(target=self.__startingMonitor,
                args=(q, deltaT, codigo))
            p.start()
            self.subprocess.append(p)

        #while subprocess:
            #subprocess.pop().join()

        #self.statusBar().showMessage('Finalizado')


def main():
    app = QtGui.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    #LZ656949203US,SW562573166BR,PG834109975BR
    main()
