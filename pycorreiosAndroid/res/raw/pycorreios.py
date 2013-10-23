#!/usr/bin/env python
__title__ = "adentregas"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "11/10/2013"
__versio__ = "0.1"


"""
Sistema de alerta de entregas automatico de pacotes enviados pelos correios
"""


from beautifulsoup import BeautifulSoup
from string import replace
import sys
import os
import imp
import shutil

import urllib2
import urllib
import time

import getopt


try:
    import pygame.mixer as mixer
except ImportError:
    
    import android

    droid = android.Android()
    
    #def mixer(myfile):
        #return droid.mediaPlay(myfile)


class adentregas:

    def __init__(self, rcode, deltat, LocalF = '/mnt/sdcard/pycorreios/',
                       locOrigin=None, alarmeLD=True, mysound='Rooster.wav'):
        url1 = 'http://websro.correios.com.br/sro_bin/txect01$.Inexistente'
        url2 = '?P_LINGUA=001&P_TIPO=002&P_COD_LIS='
        self.alarmeLD = alarmeLD
        self.url = url1 + url2
        self.rcode = rcode
        self.deltat = deltat
        self.objetoEstatus = None
        self.locOrigin = locOrigin
        self.pageEstatus = None
        self.LocalF = LocalF
        self.mysound = LocalF + \
                        'sounds/' + mysound
        self.myimage = LocalF+ \
                        'images/'
        self.__starting()

    def __starting(self):

        pycorreiosLocal = os.path.dirname(__file__) 
        
        #imp.find_module('pycorreios')[1]

        HOME = self.LocalF

        if not os.path.exists(self.LocalF):
            import zipfile
            
            if(self.locOrigin is not None):
                local = self.locOrigin
            else:
                local = os.path.dirname(__file__)
            print 'Creating .pycorreios cache diretory in %s' % HOME
            os.makedirs(self.LocalF)
            shutil.copyfile(local + '/extrafiles.zip', self.LocalF + 'extrafiles.zip')
            zip = zipfile.ZipFile(r'' + self.LocalF + 'extrafiles.zip')
            zip.extractall(self.LocalF)

    def openURL(self):

        try:
            mypage = urllib.urlopen(self.url + self.rcode)
        except:
            mypage = None
        return mypage

    def page(self):

        mypage = self.openURL()

        if(mypage is None):
            self.pageEstatus = 'Nao conectado'
            print 'Erro de Conexao'
            return None
        else:
            mypage = mypage.read()
            self.pageEstatus = mypage

        soup = BeautifulSoup(mypage)
        return soup

    def verificaNaoEncontrado(self, page):
        brs = [br for br in page.findAll("font")]
        splited = str(brs[0]).split('>')
        tmp = [sp.split('<') for sp in splited]
        naoencontrado = tmp[2][0]
        print naoencontrado
        testador = 'Objetos n\xc3\xa3o Encontrados'
#naoencontrado = naoencontrado.decode('utf-8')
        if(testador == naoencontrado):
            self.objetoEstatus = 'Objeto nao Encontrado'
            return 'Objeto nao Encontrado, verifique o seu codigo'
        else:
            return 1

    def findtable(self):
        soup = self.page()
        if(soup is not None):
            tables = [table for table in soup.findAll("table")]
            if (len(tables) >= 0):
                if(len(tables) == 1):
                    testeExiste = self.verificaNaoEncontrado(soup)

                    if(testeExiste == 1):
                        return tables[0]

                    elif(testeExiste ==
                         'Objeto nao Encontrado, verifique o seu codigo'):
                        return None

                    else:
                        print 'Erro Desconhecido'
                        return 'Erro Desconhecido'

                else:

                    page404 = [h1 for h1 in soup.findAll('h1')]
                    if(str(page404[0]) == '<h1>Not Found</h1>'):
                        self.objetoEstatus = 'Page Not Found'
                        return None
                    else:
                        return tables[0]
            else:
                return None
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
                    

                    if(teste == 'Saiu para entrega ao destinat\xc3\xa1rio' or 
			teste == 'Saiu para entrega'):
                        saiuparaentrega = True
                elif(len(tmp) == 5):
                    teste = tmp[2][0]
                    
                    
                    

                    tdDecomp.append(teste)
                    if(teste == 'Entrega Efetuada'):
                        self.objetoEstatus = 'Entrega Efetuada'
                        
                    if(teste == 'Saiu para entrega ao destinat\xc3\xa1rio'
                       or teste == 'Saiu para entrega'
                       ):
                        saiuparaentrega = True                 

                    

            if(saiuparaentrega is True and
                self.objetoEstatus == 'Entrega Efetuada'):
                return [saiuparaentrega, tdDecomp[0], tdDecomp, table]
            elif(saiuparaentrega is True and self.objetoEstatus != 'Entrega Efetuada'):
                self.objetoEstatus = 'Saiu para entrega'
                return [saiuparaentrega, tdDecomp[0], tdDecomp, table]
            else:
                return [None, tdDecomp]

    def versaiuentrega(self):
        saiuparaentrega = self.findTD()
        if(saiuparaentrega is None):
            return [None]
        if(saiuparaentrega[0] is not None):

            return saiuparaentrega[1], saiuparaentrega[2], saiuparaentrega[3]
        else:
            return ['continue']

    def alarme(self):
        if(self.alarmeLD is True):
            droid.mediaPlay(self.mysound)
        else:
            pass
        return None

    def monitorEntregas(self):

        time0 = time.time()
        print 'Sistema de Monitoramente de Encomendas Iniciado'
        dados = self.versaiuentrega()
        if(dados[0] is not None):
            if(dados[0] == 'continue'):
                print 'Objeto ainda nao saiu para entrega'
                pass
            else:
                self.alarme()
                print '''Sua Encomenda saiu para entrega
(data - hora): %s ''' % dados[0]
                return 'Sua Encomenda saiu para entrega (data - hora): %s '\
                         % dados[0], 1
        elif(dados[0] is None and self.pageEstatus == 'Nao conectado'):
            print self.pageEstatus
            return self.pageEstatus
        else:
            print self.objetoEstatus
            return self.objetoEstatus

        countConection = 0

        while(1):
            if((time.time() - time0) >= self.deltat * 60):
                time0 = time.time()
                dados = self.versaiuentrega()
                if(dados[0] is not None):
                    if(dados[0] == 'continue'):
                        countConection = 0
                        pass
                    else:
                        self.alarme()
                        print '''Sua Encomenda saiu para entrega
(data - hora): %s ''' % dados[0]
                        return '''Sua Encomenda saiu para entrega
(data - hora): %s ''' % dados[0], 1
                elif(dados[0] is None and self.pageEstatus == 'Nao conectado'):
                    print self.pageEstatus
                    countConection += 1

                if(countConection == 3):
                    return 'Erro de Conexao'

if(__name__ == '__main__'):
    #PG834109975BR
    obj = adentregas('PG834109975BR', 30.0)
    obj.monitorEntregas()


