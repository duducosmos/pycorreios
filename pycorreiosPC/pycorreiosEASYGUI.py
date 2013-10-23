#!/usr/bin/env python
__title__ = "adentregas"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "11/10/2013"
__versio__ = "0.1"


"""
Sistema de alerta de entregas automatico de pacotes enviados pelos correios
"""


from BeautifulSoup import BeautifulSoup
from string import replace
import sys
import os
import imp
import shutil

import urllib2
import urllib
import time

import getopt
import easygui as eg

import pygame

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer


class adentregas:

    def __init__(self, rcode, deltat, mysound='Rooster.wav'):
        url1 = 'http://websro.correios.com.br/sro_bin/txect01$.Inexistente'
        url2 = '?P_LINGUA=001&P_TIPO=002&P_COD_LIS='
        self.url = url1 + url2
        self.rcode = rcode
        self.deltat = deltat
        self.mysound = os.path.expanduser('~') + \
                        '/.pycorreios/sounds/' + mysound
        self.__starting()

    def __starting(self):

        pycorreiosLocal = imp.find_module('pycorreios')[1]

        HOME = os.path.expanduser('~')

        if not os.path.exists(HOME + '/.pycorreios'):

            local = os.path.dirname(pycorreiosLocal)
            print 'Creating .pycorreios cache diretory in %s' % HOME
            os.makedirs(HOME + '/.pycorreios')
            shutil.copytree(local + '/sounds', HOME + '/.pycorreios/sounds')

    def openURL(self):
        return urllib.urlopen(self.url + self.rcode)

    def page(self):
        mypage = self.openURL().read()
        soup = BeautifulSoup(mypage)
        return soup

    def verificaNaoEncontrado(self, page):
        brs = [br for br in page.findAll("font")]
        splited = str(brs[0]).split('>')
        tmp = [sp.split('<') for sp in splited]
        naoencontrado = tmp[2][0]
        testador = u'Objetos n\u0103o Encontrados'
        naoencontrado = naoencontrado.decode('utf-8')
        if(testador == naoencontrado):
            eg.msgbox('Objeto nao Encontrado, verifique o seu codigo')
            sys.exit()
        else:
            return 1

    def findtable(self):
        soup = self.page()
        tables = [table for table in soup.findAll("table")]

        if (len(tables) >= 0):
            if(len(tables) == 1):
                if(self.verificaNaoEncontrado(soup) == 1):
                    return tables[0]

            else:
                return tables[0]
        else:
            return None

    def findTD(self):
        table = self.findtable()
        saiuparaentrega = None
        if(table is not None):
            tds = [td for td in table.findAll('td')]
            #tds = tds[4:]
            tdDecomp = []

            for tdi in tds:
                splited = str(tdi).split('>')
                tmp = [sp.split('<') for sp in splited]
                if(len(tmp) == 3):
                    teste = tmp[1][0]
                    tdDecomp.append(teste)

                    if(teste == 'Saiu para entrega'):
                        saiuparaentrega = True
                elif(len(tmp) == 5):
                    teste = tmp[2][0]

                    tdDecomp.append(teste)
                    if(teste == 'Saiu para entrega'):
                        saiuparaentrega = True

            if(saiuparaentrega is True):
                return [saiuparaentrega, tdDecomp[0], tdDecomp, table]
            else:
                return [None, tdDecomp]

    def versaiuentrega(self):
        saiuparaentrega = self.findTD()
        if(saiuparaentrega is None):
            return None
        if(saiuparaentrega[0] is not None):
            return saiuparaentrega[1], saiuparaentrega[2], saiuparaentrega[3]
        else:
            return ['continue']

    def alarme(self):
        mixer.init()
        sound = mixer.Sound(self.mysound)
        sound.play()
        return None

    def monitorEntregas(self):

        time0 = time.time()
        print 'Sistema de Monitoramente de Encomendas Iniciado'
        dados = self.versaiuentrega()
        if(dados[0] is not None):
            if(dados[0] == 'continue'):
                pass
            else:
                self.alarme()
                eg.msgbox('''Sua Encomenda saiu para entrega
(data - hora): %s ''' % dados[0])
                return

        while(1):
            if((time.time() - time0) >= self.deltat * 60):
                time0 = time.time()
                dados = self.versaiuentrega()
                if(dados[0] is not None):
                    if(dados[0] == 'continue'):
                        pass
                    else:
                        self.alarme()
                        eg.msgbox('''Sua Encomenda saiu para entrega
(data - hora): %s ''' % dados[0])
                        return


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

