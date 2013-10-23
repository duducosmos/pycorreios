#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
PyCorreios.

copyright : Eduardo dos Santos Pereira. 2012.

    PyCorreios is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    PyCorreios is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'Eduardo dos Santos Pereira'
__email__ = 'pereira.somoza@gmail.com'
__data__ = '26/02/2012'
__license__ = 'General Public License - http://www.gnu.org/licenses/'


import sys
import os


# enable running this program from absolute path
PATH_SCRIPT = os.path.dirname(os.path.abspath(__file__)) 
os.chdir(PATH_SCRIPT)
print("dir changed %s" %PATH_SCRIPT )

import pycorreios


import android

droid = android.Android()

myLayout = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" 
    android:background="#ff000000">
    
    <TextView
        android:id="@+id/textView1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Entre com os Codigos de Rastreio"
        android:textAppearance="?android:attr/textAppearanceLarge" />

    <EditText
        android:id="@+id/editText1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:ems="10" >

        <requestFocus />
    </EditText>

    <TextView
        android:id="@+id/textView2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Intervalo de Tempo de Monitoramento"
        android:textAppearance="?android:attr/textAppearanceLarge" />

    <EditText
        android:id="@+id/editText3"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:ems="10"
        android:inputType="numberSigned" />

    <Button
        android:id="@+id/button1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Iniciar Monitoramento" />

    <Button
        android:id="@+id/button2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Parar Monitoramento" />

    <TextView
        android:id="@+id/textView3"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="0.47" />
        

</LinearLayout>
"""

    

    
def eventLoop():
            
    while True:
        event = droid.eventWait().result
        key = event["data"]
        if key.has_key("key"):
            if key["key"] == "4":
                return

        if event["name"] == "click":
            id = event["data"]["id"]

            if id == "button1":                
                codigo = droid.fullQueryDetail("editText1").result
                tempo = droid.fullQueryDetail("editText3").result
                
                if(codigo["text"] != "" and tempo["text"] != ""):
                    mentrega = pycorreios.adentregas(codigo["text"],
                                                       float(tempo["text"]),
                                                       locOrigin=PATH_SCRIPT)
                    resultado = mentrega.monitorEntregas()

                else:
                    resultado = "Entre com numeros"
                    
                if(len(resultado) == 2):
                    droid.fullSetProperty("textView3","text",resultado[0])
                else:
                    droid.fullSetProperty("textView3","text",resultado)
                    
            elif id =="button1":
                droid.fullSetProperty("textView3","text",'Botao 2')

            elif id == "button3":
                return
        elif event["name"] == "screen":
            if envent["data"] == "destroy":
                return

droid.fullSetTitle('Pycorreios')
droid.fullShow(myLayout)
eventLoop()
droid.fullDismiss()
