#!/usr/bin/env python
__title__ = "informacoes_qt.py"
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
from informacoesUI import Ui_Dialog, _fromUtf8


class DesignerDialog(Ui_Dialog):

    def __init__(self, Dialog):
        super(DesignerDialog, self).__init__()
        Ui_Dialog.__init__(self)
        self.setupUi(self)


def mainDialogBox(text):
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = DesignerDialog(Dialog)
    ui.setupUi(Dialog)
    ui.textEdit.setText(text)
    Dialog.show()
    sys.exit(app.exec_())

if(__name__ == '__main__'):
    mainDialogBox('Boi da cara preta')
