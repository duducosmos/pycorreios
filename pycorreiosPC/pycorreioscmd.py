#!/usr/bin/env python
__title__ = "pycorreioscmd"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "11/10/2013"
__versio__ = "0.1"


"""
Sistema de alerta de entregas automatico de pacotes enviados pelos correios
"""

from pycorreios import *

import sys
import os
import getopt
import easygui as eg


def main():
    argv = sys.argv[1:]

    if(len(argv) == 0):
        msg = '''Entre com o codigo de rastreio e o intervalo de tempo de
                monitoramento, em minutos'''
        title = 'Sistema de Monitoramento'
        fieldNames = ['Codigo de Rastreio', 'Intervalo de Tempo']
        fieldValues = eg.multenterbox(msg, title, fieldNames)
        obj = adentregas(fieldValues[0], float(fieldValues[1]))
        obj.monitorEntregas()
    else:
        uso = 'adentregas.py -r <codigo de rastreio> -t <tempo verificacao>'
        try:
            opts, args = getopt.getopt(argv, "hr:t:", ["rcode=", "dtime="])
        except getopt.GetoptError:
            print uso
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print uso
                sys.exit()
            elif opt in ("-r", "--rcode"):
                codigorastreio = arg
            elif opt in ("-t", "--dtime"):
                deltat = arg
        if(len(opts) == 0):
            print uso
            sys.exit()
        obj = adentregas(codigorastreio, float(deltat))
        obj.monitorEntregas()

if(__name__ == '__main__'):
    main()
